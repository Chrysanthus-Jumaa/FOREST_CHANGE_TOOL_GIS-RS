# 🌲 Kericho Forest Change Analysis Tool

A comprehensive Streamlit-based application for analyzing forest and land cover changes in Kericho County, Kenya from 1995-2024 using Google Earth Engine.

## 🎯 Features

- **Multi-temporal Land Cover Analysis** (1995, 2005, 2015, 2024)
- **Interactive Visualizations** with Plotly charts
- **Change Detection** with transition matrices
- **Vegetation Health Monitoring** (8 indices: NDVI, EVI, NDWI, SAVI, NBR, BSI, NDBI, MNDWI)
- **Climate Trend Analysis** (Temperature & Precipitation)
- **Interactive Maps** powered by geemap
- **Data Export** capabilities (CSV downloads)
- **Comprehensive Reporting**

## 📋 Prerequisites

- Python 3.8 or higher
- Google Earth Engine account ([Sign up here](https://earthengine.google.com/signup/))
- Your training data geometries imported in GEE

## 🚀 Installation

### Step 1: Clone or Download

```bash
# If you have the files in a directory
cd kericho-forest-tool
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Authenticate Google Earth Engine

**First time only:**

```bash
earthengine authenticate
```

This will open a browser window for you to authorize access. Follow the prompts.

## ⚙️ Configuration

### Adding Your Training Data

You need to add your actual training geometries to `gee_analysis.py`. 

Open `gee_analysis.py` and locate the `_load_training_data()` method (around line 42). Replace the `None` values with your actual geometry imports:

```python
def _load_training_data(self) -> Dict:
    """Load training geometries for each year and class."""
    
    # Import your geometries here
    # Example format:
    # forest1995 = ee.Geometry.MultiPoint([[35.28, -0.37], [35.30, -0.38], ...])
    
    training = {
        1995: {
            'forest': forest1995,      # Replace with your geometry
            'tea': tea1995,            # Replace with your geometry
            'otherveg': otherveg1995,  # Replace with your geometry
            'bare': bare1995,          # Replace with your geometry
            'builtup': builtup1995     # Replace with your geometry
        },
        2005: {
            'forest': forest2005,
            'tea': tea2005,
            'otherveg': otherveg2005,
            'bare': bare2005,
            'builtup': builtup2005
        },
        2015: {
            'forest': forest2015,
            'tea': tea2015,
            'otherveg': otherveg2015,
            'bare': bare2015,
            'builtup': builtup2015
        },
        2024: {
            'forest': forest2024,
            'tea': tea2024,
            'otherveg': otherveg2024,
            'bare': bare2024,
            'builtup': builtup2024
        },
    }
    return training
```

### Alternative: Export from GEE Code Editor

If your geometries are in the GEE Code Editor, you can export them as GeoJSON and load them:

```python
# In your script
forest1995 = ee.Geometry(ee.FeatureCollection('users/yourusername/forest1995').geometry())
```

## 🎮 Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📱 Using the Tool

### 1. Initialize Analysis
- Click **"🚀 Initialize Analysis"** in the sidebar
- Wait 1-2 minutes for GEE to process 30 years of data
- Progress will be displayed

### 2. Select Analysis Mode

Choose from 5 analysis modes:

#### 🏠 Home
- Quick overview dashboard
- Key metrics and trends
- Summary visualizations

#### 📈 Land Cover Statistics
- Detailed area statistics for all classes
- Stacked bar charts
- Individual class trends
- Pie charts by year
- Interactive map viewer

#### 🔄 Change Detection
- Select any two years to compare
- View transition matrices
- Horizontal bar charts showing change magnitude
- Multi-period comparison tabs

#### 🌿 Vegetation Indices
- Track 8 vegetation health indices
- Multi-line trend charts
- Spatial visualization on map
- Index descriptions and interpretations

#### 🌤️ Climate Analysis
- Temperature and precipitation trends
- Dual-axis charts
- Individual trend analysis
- Spatial climate patterns

#### 📋 Comprehensive Report
- Executive summary
- All analyses in one place
- Tabbed interface
- Export all data

### 3. Export Data
- Most views have **"📥 Download"** buttons
- Export as CSV for further analysis
- Timestamped filenames

## 🗂️ Project Structure

```
kericho-forest-tool/
│
├── app.py                 # Main Streamlit application
├── gee_analysis.py        # Core GEE analysis logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Technical Details

### Data Sources
- **Landsat 5 TM** (1995, 2005)
- **Landsat 7 ETM+** (2005)
- **Landsat 8 OLI** (2015)
- **Landsat 9 OLI-2** (2024)
- **CHIRPS** - Daily precipitation
- **MODIS MOD11A2** - Land surface temperature

### Classification Method
- **Algorithm:** Random Forest (100 trees)
- **Classes:** 5 (Forest, Tea Plantations, Other Vegetation, Bare Soil/Land, Built-up)
- **Resolution:** 30m (Landsat)

### Vegetation Indices
- NDVI, EVI, NDWI, SAVI, NBR, BSI, NDBI, MNDWI

## 🐛 Troubleshooting

### "GEE Authentication failed"
```bash
# Re-authenticate
earthengine authenticate
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Slow performance
- First run initializes all data (1-2 mins)
- Subsequent analyses are cached
- Complex operations (change detection) take longer

### Map not displaying
- Check internet connection (geemap needs online tiles)
- Try refreshing the page
- Check browser console for errors

## 💡 Tips

1. **First Run:** Allow 1-2 minutes for initialization
2. **Caching:** Once initialized, switching between modes is instant
3. **Exports:** Download data for offline analysis
4. **Year Selection:** Use dropdowns to compare specific years
5. **Multi-select:** Hold Ctrl/Cmd to select multiple indices/classes

## 📊 Output Examples

### Land Cover Areas (km²)
| Year | Forest | Tea | Other Veg | Bare | Built-up |
|------|--------|-----|-----------|------|----------|
| 1995 | 450.2  | 320.5 | 180.3   | 25.1 | 15.8    |
| 2024 | 412.8  | 355.2 | 165.4   | 28.9 | 29.6    |

### Change Detection
| From | To | Area (km²) |
|------|----|------------|
| Forest | Tea Plantations | 45.3 |
| Other Vegetation | Built-up | 12.7 |

## 🔮 Future Enhancements

Possible additions:
- [ ] Multiple county support
- [ ] Custom AOI upload
- [ ] Accuracy assessment module
- [ ] PDF report generation
- [ ] Time series animation
- [ ] Additional satellite sensors

## 📝 Notes

- **Training Data:** You must add your own training geometries
- **GEE Quota:** Heavy usage may hit GEE computation limits
- **Internet Required:** Tool needs connection to GEE servers
- **Browser:** Works best in Chrome/Firefox

## 📧 Support

For issues or questions:
1. Check GEE authentication
2. Verify training data is properly loaded
3. Review error messages in terminal
4. Check GEE Code Editor for geometry access

## 📄 License

This tool uses Google Earth Engine which has its own terms of service. Ensure compliance with:
- [GEE Terms of Service](https://earthengine.google.com/terms/)
- Proper citation of data sources

## 🙏 Acknowledgments

- **Data:** NASA/USGS (Landsat), UCSB-CHG (CHIRPS), NASA (MODIS)
- **Platform:** Google Earth Engine
- **UI Framework:** Streamlit
- **Mapping:** geemap by Qiusheng Wu

---

**Ready to analyze Kericho's forests!** 🌲📊🗺️