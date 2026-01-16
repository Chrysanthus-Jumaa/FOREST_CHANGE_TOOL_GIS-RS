"""
Google Earth Engine Analysis Module for Kericho Forest Tool
Converted from JavaScript to Python
"""

import ee
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class KerichoForestAnalysis:
    """Main analysis class for Kericho County forest change detection."""
    
    def __init__(self):
        """Initialize the analysis with constants and configurations."""
        self.class_colors = ['006400', '90EE90', 'ADFF2F', 'D2B48C', 'FF0000']
        self.class_names = ['Forest', 'Tea Plantations', 'Other Vegetation', 'Bare Soil/Land', 'Built-up']
        self.years = [1995, 2005, 2015, 2024]
        
        # Load Kericho boundary
        self.kericho = ee.FeatureCollection("projects/ee-chrysanthusjumaa23/assets/counties") \
            .filter(ee.Filter.eq('COUNTY_NAM', 'KERICHO'))
        
        # Training data (imported geometries)
        self.training_data = self._load_training_data()
        
        # Store processed images
        self.images = {}
        self.indices = {}
        self.classified = {}
        self.climate = {}
        
    def _load_training_data(self) -> Dict:
        """Load training geometries from GEE assets."""
        
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURATION: Update this with your GEE username
        # ═══════════════════════════════════════════════════════════════════
        GEE_USERNAME = 'ee-chrysanthusjumaa23'  # ← CHANGE THIS TO YOUR USERNAME
        
        # Base path for training assets
        base_path = f'users/{GEE_USERNAME}/kericho_training'
        
        # ═══════════════════════════════════════════════════════════════════
        # Load training points from GEE assets
        # ═══════════════════════════════════════════════════════════════════
        
        def load_class_geometry(year, class_name):
            """Load a specific class geometry from GEE asset."""
            try:
                asset_path = f'{base_path}/{class_name}_{year}'
                fc = ee.FeatureCollection(asset_path)
                return fc.geometry()
            except Exception as e:
                print(f"Warning: Could not load {class_name}_{year} from {asset_path}")
                print(f"Error: {e}")
                return None
        
        training = {
            1995: {
                'forest': load_class_geometry(1995, 'forest'),
                'tea': load_class_geometry(1995, 'tea'),
                'otherveg': load_class_geometry(1995, 'otherveg'),
                'bare': load_class_geometry(1995, 'bare'),
                'builtup': load_class_geometry(1995, 'builtup'),
            },
            2005: {
                'forest': load_class_geometry(2005, 'forest'),
                'tea': load_class_geometry(2005, 'tea'),
                'otherveg': load_class_geometry(2005, 'otherveg'),
                'bare': load_class_geometry(2005, 'bare'),
                'builtup': load_class_geometry(2005, 'builtup'),
            },
            2015: {
                'forest': load_class_geometry(2015, 'forest'),
                'tea': load_class_geometry(2015, 'tea'),
                'otherveg': load_class_geometry(2015, 'otherveg'),
                'bare': load_class_geometry(2015, 'bare'),
                'builtup': load_class_geometry(2015, 'builtup'),
            },
            2024: {
                'forest': load_class_geometry(2024, 'forest'),
                'tea': load_class_geometry(2024, 'tea'),
                'otherveg': load_class_geometry(2024, 'otherveg'),
                'bare': load_class_geometry(2024, 'bare'),
                'builtup': load_class_geometry(2024, 'builtup'),
            },
        }
        
        return training
    
    def initialize_analysis(self, progress_callback=None):
        """
        Run the complete initialization: load imagery, calculate indices, classify.
        
        Args:
            progress_callback: Optional function to report progress
        """
        if progress_callback:
            progress_callback("Loading satellite imagery...")
        
        self._load_imagery()
        
        if progress_callback:
            progress_callback("Calculating vegetation indices...")
        
        self._calculate_indices()
        
        if progress_callback:
            progress_callback("Running classifications...")
        
        self._classify_images()
        
        if progress_callback:
            progress_callback("Loading climate data...")
        
        self._load_climate_data()
        
        if progress_callback:
            progress_callback("Analysis ready!")
    
    def _mask_l457sr(self, image: ee.Image) -> ee.Image:
        """Cloud masking for Landsat 4/5/7."""
        qa_mask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
        saturation_mask = image.select('QA_RADSAT').eq(0)
        return image.updateMask(qa_mask).updateMask(saturation_mask)
    
    def _mask_l89sr(self, image: ee.Image) -> ee.Image:
        """Cloud masking for Landsat 8/9."""
        qa_mask = image.select('QA_PIXEL').bitwiseAnd(int('11111', 2)).eq(0)
        saturation_mask = image.select('QA_RADSAT').eq(0)
        return image.updateMask(qa_mask).updateMask(saturation_mask)
    
    def _get_clean_composite(self, year: int, start_month: int, end_month: int, 
                            collection: ee.ImageCollection, mask_func) -> ee.Image:
        """Create cloud-free composite for a given year."""
        start_date = ee.Date.fromYMD(year, start_month, 1)
        end_date = ee.Date.fromYMD(year, end_month, 28)
        
        composite = collection.filterDate(start_date, end_date) \
            .filterBounds(self.kericho) \
            .map(mask_func) \
            .median() \
            .clip(self.kericho)
        
        return composite
    
    def _load_imagery(self):
        """Load Landsat imagery for all years."""
        l5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
        l7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
        l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
        
        self.images[1995] = self._get_clean_composite(1995, 1, 12, l5, self._mask_l457sr)
        self.images[2005] = self._get_clean_composite(2005, 1, 12, l7, self._mask_l457sr)
        self.images[2015] = self._get_clean_composite(2015, 1, 12, l8, self._mask_l89sr)
        self.images[2024] = self._get_clean_composite(2024, 1, 12, l9, self._mask_l89sr)
    
    def _calculate_indices_l457(self, image: ee.Image) -> ee.Image:
        """Calculate vegetation indices for Landsat 4/5/7."""
        ndvi = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
        ndwi = image.normalizedDifference(['SR_B4', 'SR_B5']).rename('NDWI')
        
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
            {
                'NIR': image.select('SR_B4'),
                'RED': image.select('SR_B3'),
                'BLUE': image.select('SR_B1')
            }
        ).rename('EVI')
        
        savi = image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
            {
                'NIR': image.select('SR_B4'),
                'RED': image.select('SR_B3')
            }
        ).rename('SAVI')
        
        nbr = image.normalizedDifference(['SR_B4', 'SR_B7']).rename('NBR')
        
        bsi = image.expression(
            '((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))',
            {
                'SWIR': image.select('SR_B5'),
                'RED': image.select('SR_B3'),
                'NIR': image.select('SR_B4'),
                'BLUE': image.select('SR_B1')
            }
        ).rename('BSI')
        
        ndbi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDBI')
        mndwi = image.normalizedDifference(['SR_B2', 'SR_B5']).rename('MNDWI')
        
        return image.addBands([ndvi, ndwi, evi, savi, nbr, bsi, ndbi, mndwi])
    
    def _calculate_indices_l89(self, image: ee.Image) -> ee.Image:
        """Calculate vegetation indices for Landsat 8/9."""
        ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
        ndwi = image.normalizedDifference(['SR_B5', 'SR_B6']).rename('NDWI')
        
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
            {
                'NIR': image.select('SR_B5'),
                'RED': image.select('SR_B4'),
                'BLUE': image.select('SR_B2')
            }
        ).rename('EVI')
        
        savi = image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
            {
                'NIR': image.select('SR_B5'),
                'RED': image.select('SR_B4')
            }
        ).rename('SAVI')
        
        nbr = image.normalizedDifference(['SR_B5', 'SR_B7']).rename('NBR')
        
        bsi = image.expression(
            '((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))',
            {
                'SWIR': image.select('SR_B6'),
                'RED': image.select('SR_B4'),
                'NIR': image.select('SR_B5'),
                'BLUE': image.select('SR_B2')
            }
        ).rename('BSI')
        
        ndbi = image.normalizedDifference(['SR_B6', 'SR_B5']).rename('NDBI')
        mndwi = image.normalizedDifference(['SR_B3', 'SR_B6']).rename('MNDWI')
        
        return image.addBands([ndvi, ndwi, evi, savi, nbr, bsi, ndbi, mndwi])
    
    def _calculate_indices(self):
        """Calculate indices for all years."""
        self.indices[1995] = self._calculate_indices_l457(self.images[1995])
        self.indices[2005] = self._calculate_indices_l457(self.images[2005])
        self.indices[2015] = self._calculate_indices_l89(self.images[2015])
        self.indices[2024] = self._calculate_indices_l89(self.images[2024])
    
    def _prepare_training(self, forest, tea, otherveg, bare, builtup) -> ee.FeatureCollection:
        """Prepare training data from geometries."""
        def create_features(geom, class_value):
            if geom is None:
                return ee.FeatureCollection([])
            return ee.FeatureCollection(
                geom.geometries().map(
                    lambda g: ee.Feature(ee.Geometry(g), {'landcover': class_value})
                )
            )
        
        forest_fc = create_features(forest, 0)
        tea_fc = create_features(tea, 1)
        otherveg_fc = create_features(otherveg, 2)
        bare_fc = create_features(bare, 3)
        builtup_fc = create_features(builtup, 4)
        
        return forest_fc.merge(tea_fc).merge(otherveg_fc).merge(bare_fc).merge(builtup_fc)
    
    def _classify_image(self, image: ee.Image, training: ee.FeatureCollection, 
                       bands: List[str]) -> ee.Image:
        """Classify an image using Random Forest."""
        training_data = image.select(bands).sampleRegions(
            collection=training,
            properties=['landcover'],
            scale=30
        )
        
        classifier = ee.Classifier.smileRandomForest(100).train(
            features=training_data,
            classProperty='landcover',
            inputProperties=bands
        )
        
        return image.select(bands).classify(classifier)
    
    def _classify_images(self):
        """Classify all years."""
        bands_457 = ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7']
        bands_89 = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']
        
        for year in self.years:
            training_year = self.training_data[year]
            training = self._prepare_training(
                training_year['forest'],
                training_year['tea'],
                training_year['otherveg'],
                training_year['bare'],
                training_year['builtup']
            )
            
            if year in [1995, 2005]:
                self.classified[year] = self._classify_image(self.images[year], training, bands_457)
            else:
                self.classified[year] = self._classify_image(self.images[year], training, bands_89)
    
    def _load_climate_data(self):
        """Load climate data for all years."""
        chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
        modis_lst = ee.ImageCollection('MODIS/061/MOD11A2')
        
        for year in self.years:
            start_date = ee.Date.fromYMD(year, 1, 1)
            end_date = ee.Date.fromYMD(year, 12, 31)
            
            # Precipitation (CHIRPS available from 1981)
            precip = chirps.filterDate(start_date, end_date) \
                .filterBounds(self.kericho) \
                .sum() \
                .clip(self.kericho) \
                .rename('precipitation')
            
            # Temperature (MODIS only available from 2000 onwards)
            # For years before 2000, use a constant placeholder or skip
            if year >= 2000:
                temp = modis_lst.filterDate(start_date, end_date) \
                    .filterBounds(self.kericho) \
                    .select('LST_Day_1km') \
                    .mean() \
                    .multiply(0.02) \
                    .subtract(273.15) \
                    .clip(self.kericho) \
                    .rename('temperature')
                
                self.climate[year] = ee.Image.cat([precip, temp])
            else:
                # For years before 2000, only store precipitation
                # Create a dummy temperature band with None/masked values
                temp = ee.Image.constant(-9999).clip(self.kericho).rename('temperature')
                self.climate[year] = ee.Image.cat([precip, temp])
    
    def calculate_land_cover_areas(self) -> pd.DataFrame:
        """
        Calculate land cover areas for all years.
        
        Returns:
            DataFrame with areas in km² for each class and year
        """
        results = []
        
        for year in self.years:
            area_image = ee.Image.pixelArea().addBands(self.classified[year])
            
            areas = area_image.reduceRegion(
                reducer=ee.Reducer.sum().group(
                    groupField=1,
                    groupName='class'
                ),
                geometry=self.kericho.geometry(),
                scale=30,
                maxPixels=1e13
            )
            
            # Convert to dictionary
            area_list = areas.getInfo()['groups']
            
            year_areas = {class_name: 0.0 for class_name in self.class_names}
            
            for item in area_list:
                class_id = item['class']
                area_km2 = item['sum'] / 1_000_000  # Convert m² to km²
                year_areas[self.class_names[class_id]] = round(area_km2, 2)
            
            year_areas['Year'] = year
            results.append(year_areas)
        
        df = pd.DataFrame(results)
        return df[['Year'] + self.class_names]
    
    def calculate_change_matrix(self, year_from: int, year_to: int) -> pd.DataFrame:
        """
        Calculate change detection matrix between two years.
        
        Args:
            year_from: Starting year
            year_to: Ending year
            
        Returns:
            DataFrame with significant transitions
        """
        class1 = self.classified[year_from]
        class2 = self.classified[year_to]
        
        combined = class1.multiply(10).add(class2)
        change_area = ee.Image.pixelArea().addBands(combined)
        
        changes = change_area.reduceRegion(
            reducer=ee.Reducer.sum().group(
                groupField=1,
                groupName='change'
            ),
            geometry=self.kericho.geometry(),
            scale=30,
            maxPixels=1e13
        )
        
        change_list = changes.getInfo()['groups']
        
        results = []
        for item in change_list:
            from_class = int(item['change']) // 10
            to_class = int(item['change']) % 10
            area_km2 = item['sum'] / 1_000_000
            
            # Only include significant changes (>1 km² and actual change)
            if from_class != to_class and area_km2 > 1:
                results.append({
                    'From': self.class_names[from_class],
                    'To': self.class_names[to_class],
                    'Area (km²)': round(area_km2, 2),
                    'From_Class_ID': from_class
                })
        
        df = pd.DataFrame(results)
        if len(df) > 0:
            df = df.sort_values('Area (km²)', ascending=False)
        
        return df
    
    def get_vegetation_indices_trends(self) -> pd.DataFrame:
        """
        Get mean vegetation indices for all years.
        
        Returns:
            DataFrame with index values over time
        """
        indices_list = ['NDVI', 'EVI', 'NDWI', 'SAVI', 'NBR', 'BSI', 'NDBI', 'MNDWI']
        results = []
        
        for year in self.years:
            year_data = {'Year': year}
            
            for index_name in indices_list:
                mean_val = self.indices[year].select(index_name).reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=self.kericho.geometry(),
                    scale=500,
                    maxPixels=1e13
                ).getInfo()
                
                year_data[index_name] = mean_val.get(index_name)
            
            results.append(year_data)
        
        return pd.DataFrame(results)
    
    def get_climate_trends(self) -> pd.DataFrame:
        """
        Get climate data trends for all years.
        
        Returns:
            DataFrame with temperature and precipitation over time
        """
        results = []
        
        for year in self.years:
            temp_mean = self.climate[year].select('temperature').reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.kericho.geometry(),
                scale=1000,
                maxPixels=1e13
            ).getInfo()
            
            precip_mean = self.climate[year].select('precipitation').reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.kericho.geometry(),
                scale=1000,
                maxPixels=1e13
            ).getInfo()
            
            # Handle missing temperature data (years before 2000)
            temp_value = temp_mean.get('temperature')
            if temp_value is not None and temp_value != -9999:
                temp_display = temp_value
            else:
                temp_display = None  # Will show as NaN in dataframe
            
            results.append({
                'Year': year,
                'Temperature (°C)': temp_display,
                'Precipitation (mm)': precip_mean.get('precipitation')
            })
        
        return pd.DataFrame(results)
    
    def get_map_layers(self) -> Dict:
        """
        Get map visualization layers for the interactive map.
        
        Returns:
            Dictionary containing ee.Image objects and visualization parameters
        """
        return {
            'kericho_boundary': self.kericho,
            'classified_images': self.classified,
            'indices_images': self.indices,
            'climate_images': self.climate,
            'vis_params': {
                'classified': {
                    'min': 0,
                    'max': 4,
                    'palette': self.class_colors
                },
                'ndvi': {'min': -0.2, 'max': 0.8, 'palette': ['ff0000', 'ffff00', '00ff00']},
                'evi': {'min': -0.2, 'max': 0.8, 'palette': ['8B4513', 'ffff00', '00ff00']},
                'ndwi': {'min': -0.5, 'max': 0.5, 'palette': ['8B4513', 'ffffff', '0000ff']},
                'temperature': {'min': 15, 'max': 35, 'palette': ['0000ff', 'ffffff', 'ff0000']},
                'precipitation': {'min': 800, 'max': 2000, 'palette': ['ffffff', '0000ff', '00008b']}
            }
        }