"""
Kericho Forest Change Analysis Tool
Streamlit Application - Main Interface
"""

import streamlit as st
import ee
import geemap.foliumap as geemap
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import time

from gee_analysis import KerichoForestAnalysis


# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Kericho Forest Analysis",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #2d5016 0%, #4a7c23 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2d5016;
    }
    .stButton>button {
        background-color: #2d5016;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4a7c23;
    }
    </style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# INITIALIZE GEE & SESSION STATE
# ═══════════════════════════════════════════════════════════════════

@st.cache_resource
def initialize_gee():
    """Initialize Google Earth Engine."""
    try:
        # Check if running on Streamlit Cloud with service account
        if 'gee' in st.secrets:
            # Use service account from secrets
            credentials = ee.ServiceAccountCredentials(
                email=st.secrets['gee']['client_email'],
                key_data=st.secrets['gee']['private_key']
            )
            ee.Initialize(
                credentials=credentials,
                project='ee-chrysanthusjumaa23'
            )
            return True
        else:
            # Local development - use default authentication
            ee.Initialize(project='ee-chrysanthusjumaa23')
            return True
    except Exception as e:
        st.error(f"⚠️ GEE Initialization failed: {e}")
        st.info("Check service account credentials in Streamlit Cloud secrets")
        return False
@st.cache_resource
def get_analysis_object():
    """Get cached analysis object."""
    return KerichoForestAnalysis()


# Initialize
gee_initialized = initialize_gee()

if not gee_initialized:
    st.error("⚠️ Google Earth Engine initialization failed. Please authenticate.")
    st.stop()

# Session state initialization
if 'analysis_ready' not in st.session_state:
    st.session_state.analysis_ready = False
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None


# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
    <div class="main-header">
        <h1>🌲 Kericho Forest Change Analysis Tool</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">
            Multi-temporal Land Cover Analysis System (1995-2024)
        </p>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2d5016/ffffff?text=Kericho+County", 
             use_container_width=True)
    
    st.markdown("### 📊 Analysis Control Panel")
    
    # Initialize Analysis Button
    if not st.session_state.analysis_ready:
        if st.button("🚀 Initialize Analysis", type="primary", use_container_width=True):
            with st.spinner("Initializing GEE analysis..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def progress_callback(message):
                    status_text.text(message)
                    time.sleep(0.5)
                
                analyzer = get_analysis_object()
                
                # Progress simulation (GEE operations happen server-side)
                progress_bar.progress(20)
                status_text.text("Loading satellite imagery...")
                time.sleep(1)
                
                progress_bar.progress(50)
                status_text.text("Calculating vegetation indices...")
                time.sleep(1)
                
                progress_bar.progress(80)
                status_text.text("Running classifications...")
                time.sleep(1)
                
                # Actually run the initialization
                analyzer.initialize_analysis(progress_callback)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis ready!")
                
                st.session_state.analyzer = analyzer
                st.session_state.analysis_ready = True
                time.sleep(1)
                st.rerun()
    else:
        st.success("✅ Analysis Initialized")
        
        st.markdown("---")
        
        # Analysis Mode Selection
        analysis_mode = st.radio(
            "Select Analysis Mode:",
            [
                "🏠 Home",
                "📈 Land Cover Statistics",
                "🔄 Change Detection",
                "🌿 Vegetation Indices",
                "🌤️ Climate Analysis",
                "📋 Comprehensive Report"
            ],
            index=0
        )
        
        st.markdown("---")
        
        # Legend
        st.markdown("### 🎨 Land Cover Legend")
        class_colors_hex = ['#006400', '#90EE90', '#ADFF2F', '#D2B48C', '#FF0000']
        class_names = ['Forest', 'Tea Plantations', 'Other Vegetation', 'Bare Soil/Land', 'Built-up']
        
        for color, name in zip(class_colors_hex, class_names):
            st.markdown(f'<span style="color:{color}">⬛</span> {name}', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Info
        st.markdown("### ℹ️ About")
        st.info("""
        **Study Area:** Kericho County, Kenya
        
        **Time Period:** 1995 - 2024
        
        **Data Sources:**
        - Landsat 5/7/8/9
        - CHIRPS Precipitation
        - MODIS Land Surface Temperature
        
        **Analysis Methods:**
        - Random Forest Classification
        - Multi-temporal Change Detection
        - Vegetation Index Analysis
        """)


# ═══════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════════

if not st.session_state.analysis_ready:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👋 Welcome!")
        st.markdown("""
        This tool provides comprehensive forest and land cover change analysis 
        for Kericho County, Kenya from 1995 to 2024.
        
        **Features:**
        - 🗺️ Interactive land cover maps
        - 📊 Statistical analysis and charts
        - 🔄 Change detection matrices
        - 🌿 Vegetation health monitoring
        - 🌤️ Climate trend analysis
        
        **To get started:**
        Click the "🚀 Initialize Analysis" button in the sidebar.
        
        ⚠️ *Note: Initial analysis may take 1-2 minutes as we process 30 years 
        of satellite data.*
        """)
        
        st.image("https://via.placeholder.com/800x400/2d5016/ffffff?text=Forest+Analysis+Tool", 
                 use_container_width=True)

else:
    analyzer = st.session_state.analyzer
    
    # ═══════════════════════════════════════════════════════════════════
    # HOME DASHBOARD
    # ═══════════════════════════════════════════════════════════════════
    
    if analysis_mode == "🏠 Home":
        st.markdown("## 📊 Quick Overview Dashboard")
        
        # Fetch land cover data
        with st.spinner("Loading overview data..."):
            lc_data = analyzer.calculate_land_cover_areas()
        
        # Latest year metrics
        latest_year = lc_data[lc_data['Year'] == 2024].iloc[0]
        first_year = lc_data[lc_data['Year'] == 1995].iloc[0]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            forest_2024 = latest_year['Forest']
            forest_1995 = first_year['Forest']
            forest_change = ((forest_2024 - forest_1995) / forest_1995 * 100)
            
            st.metric(
                label="🌲 Forest Cover (2024)",
                value=f"{forest_2024:.0f} km²",
                delta=f"{forest_change:+.1f}% since 1995"
            )
        
        with col2:
            tea_2024 = latest_year['Tea Plantations']
            tea_1995 = first_year['Tea Plantations']
            tea_change = ((tea_2024 - tea_1995) / tea_1995 * 100)
            
            st.metric(
                label="🍃 Tea Plantations (2024)",
                value=f"{tea_2024:.0f} km²",
                delta=f"{tea_change:+.1f}% since 1995"
            )
        
        with col3:
            builtup_2024 = latest_year['Built-up']
            builtup_1995 = first_year['Built-up']
            builtup_change = ((builtup_2024 - builtup_1995) / builtup_1995 * 100)
            
            st.metric(
                label="🏘️ Built-up Areas (2024)",
                value=f"{builtup_2024:.0f} km²",
                delta=f"{builtup_change:+.1f}% since 1995"
            )
        
        with col4:
            total_area = sum([latest_year[c] for c in analyzer.class_names])
            st.metric(
                label="📍 Total Study Area",
                value=f"{total_area:.0f} km²",
                delta="Kericho County"
            )
        
        st.markdown("---")
        
        # Quick visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Land Cover Trends")
            
            fig = go.Figure()
            
            for class_name in analyzer.class_names:
                fig.add_trace(go.Scatter(
                    x=lc_data['Year'],
                    y=lc_data[class_name],
                    mode='lines+markers',
                    name=class_name,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Area (km²)",
                hovermode='x unified',
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Current Distribution (2024)")
            
            pie_data = {k: v for k, v in latest_year.items() if k != 'Year'}
            
            fig = go.Figure(data=[go.Pie(
                labels=list(pie_data.keys()),
                values=list(pie_data.values()),
                hole=0.4,
                marker=dict(colors=['#006400', '#90EE90', '#ADFF2F', '#D2B48C', '#FF0000'])
            )])
            
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
    
    
    # ═══════════════════════════════════════════════════════════════════
    # LAND COVER STATISTICS
    # ═══════════════════════════════════════════════════════════════════
    
    elif analysis_mode == "📈 Land Cover Statistics":
        st.markdown("## 📈 Land Cover Statistics & Trends")
        
        with st.spinner("Calculating land cover areas..."):
            lc_data = analyzer.calculate_land_cover_areas()
        
        # Display data table
        st.markdown("### 📋 Area Statistics (km²)")
        st.dataframe(lc_data, use_container_width=True, height=200)
        
        # Download button
        csv = lc_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"kericho_landcover_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Stacked bar chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Stacked Distribution by Year")
            
            fig = go.Figure()
            
            for class_name in analyzer.class_names:
                fig.add_trace(go.Bar(
                    name=class_name,
                    x=lc_data['Year'],
                    y=lc_data[class_name],
                ))
            
            fig.update_layout(
                barmode='stack',
                xaxis_title="Year",
                yaxis_title="Area (km²)",
                height=450,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Individual Class Trends")
            
            selected_classes = st.multiselect(
                "Select classes to display:",
                analyzer.class_names,
                default=['Forest', 'Tea Plantations']
            )
            
            fig = go.Figure()
            
            for class_name in selected_classes:
                fig.add_trace(go.Scatter(
                    x=lc_data['Year'],
                    y=lc_data[class_name],
                    mode='lines+markers',
                    name=class_name,
                    line=dict(width=3),
                    marker=dict(size=10)
                ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Area (km²)",
                height=450,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Pie charts for each year
        st.markdown("---")
        st.markdown("### 🥧 Distribution by Year")
        
        cols = st.columns(4)
        
        for idx, year in enumerate(analyzer.years):
            with cols[idx]:
                year_data = lc_data[lc_data['Year'] == year].iloc[0]
                pie_data = {k: v for k, v in year_data.items() if k != 'Year'}
                
                fig = go.Figure(data=[go.Pie(
                    labels=list(pie_data.keys()),
                    values=list(pie_data.values()),
                    hole=0.3,
                    marker=dict(colors=['#006400', '#90EE90', '#ADFF2F', '#D2B48C', '#FF0000'])
                )])
                
                fig.update_layout(
                    title=str(year),
                    height=300,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Interactive map
        st.markdown("---")
        st.markdown("### 🗺️ Interactive Map Viewer")
        
        map_year = st.selectbox("Select year to display:", analyzer.years, index=3)
        
        # Create map
        Map = geemap.Map(center=[-0.37, 35.28], zoom=10)
        
        # Add boundary
        Map.addLayer(analyzer.kericho, {}, 'Study Area', opacity=0.5)
        
        # Add classified layer
        vis_params = {
            'min': 0,
            'max': 4,
            'palette': analyzer.class_colors
        }
        Map.addLayer(analyzer.classified[map_year], vis_params, f'{map_year} Land Cover')
        
        Map.to_streamlit(height=600)
    
    
    # ═══════════════════════════════════════════════════════════════════
    # CHANGE DETECTION
    # ═══════════════════════════════════════════════════════════════════
    
    elif analysis_mode == "🔄 Change Detection":
        st.markdown("## 🔄 Land Cover Change Detection")
        
        # Period selection
        col1, col2 = st.columns(2)
        
        with col1:
            year_from = st.selectbox("From Year:", analyzer.years, index=0)
        
        with col2:
            year_to = st.selectbox("To Year:", analyzer.years, index=3)
        
        if year_from >= year_to:
            st.warning("⚠️ 'To Year' must be after 'From Year'")
        else:
            with st.spinner(f"Analyzing changes from {year_from} to {year_to}..."):
                change_df = analyzer.calculate_change_matrix(year_from, year_to)
            
            if len(change_df) == 0:
                st.info(f"ℹ️ No significant changes detected (>1 km²) between {year_from} and {year_to}")
            else:
                st.markdown(f"### 📊 Significant Changes ({year_from} → {year_to})")
                
                # Display table
                st.dataframe(change_df[['From', 'To', 'Area (km²)']], use_container_width=True)
                
                # Download button
                csv = change_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Changes (CSV)",
                    data=csv,
                    file_name=f"kericho_changes_{year_from}_{year_to}.csv",
                    mime="text/csv"
                )
                
                st.markdown("---")
                
                # Horizontal bar chart
                st.markdown("### 📊 Change Magnitude")
                
                change_df['Transition'] = change_df['From'] + ' → ' + change_df['To']
                
                # Color by source class
                color_map = {
                    0: '#006400',
                    1: '#90EE90',
                    2: '#ADFF2F',
                    3: '#D2B48C',
                    4: '#FF0000'
                }
                change_df['Color'] = change_df['From_Class_ID'].map(color_map)
                
                fig = go.Figure(go.Bar(
                    x=change_df['Area (km²)'],
                    y=change_df['Transition'],
                    orientation='h',
                    marker=dict(color=change_df['Color']),
                    text=change_df['Area (km²)'],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    xaxis_title="Area (km²)",
                    yaxis_title="Land Cover Transition",
                    height=max(400, len(change_df) * 40),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Multi-period comparison
        st.markdown("---")
        st.markdown("### 📅 Multi-Period Comparison")
        
        periods = [
            (1995, 2005, "1995-2005"),
            (2005, 2015, "2005-2015"),
            (2015, 2024, "2015-2024"),
            (1995, 2024, "1995-2024 (Overall)")
        ]
        
        all_changes = {}
        
        with st.spinner("Calculating all periods..."):
            for from_yr, to_yr, label in periods:
                change_matrix = analyzer.calculate_change_matrix(from_yr, to_yr)
                if len(change_matrix) > 0:
                    all_changes[label] = change_matrix
        
        if all_changes:
            tabs = st.tabs(list(all_changes.keys()))
            
            for idx, (period, df) in enumerate(all_changes.items()):
                with tabs[idx]:
                    st.dataframe(df[['From', 'To', 'Area (km²)']], use_container_width=True)
                    
                    df['Transition'] = df['From'] + ' → ' + df['To']
                    
                    fig = go.Figure(go.Bar(
                        x=df['Area (km²)'],
                        y=df['Transition'],
                        orientation='h',
                        marker=dict(color='#2d5016'),
                        text=df['Area (km²)'],
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title=f"Changes during {period}",
                        xaxis_title="Area (km²)",
                        yaxis_title="Transition",
                        height=max(300, len(df) * 35),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    
    # ═══════════════════════════════════════════════════════════════════
    # VEGETATION INDICES
    # ═══════════════════════════════════════════════════════════════════
    
    elif analysis_mode == "🌿 Vegetation Indices":
        st.markdown("## 🌿 Vegetation Health Analysis")
        
        with st.spinner("Calculating vegetation indices..."):
            veg_data = analyzer.get_vegetation_indices_trends()
        
        st.markdown("### 📋 Index Values Over Time")
        st.dataframe(veg_data, use_container_width=True)
        
        # Download
        csv = veg_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Index Data (CSV)",
            data=csv,
            file_name=f"kericho_vegetation_indices_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Multi-line chart
        st.markdown("### 📈 Vegetation Index Trends")
        
        indices_to_plot = st.multiselect(
            "Select indices to display:",
            ['NDVI', 'EVI', 'NDWI', 'SAVI', 'NBR', 'BSI', 'NDBI', 'MNDWI'],
            default=['NDVI', 'EVI', 'NDWI']
        )
        
        fig = go.Figure()
        
        for index in indices_to_plot:
            fig.add_trace(go.Scatter(
                x=veg_data['Year'],
                y=veg_data[index],
                mode='lines+markers',
                name=index,
                line=dict(width=3),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Index Value",
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Index descriptions
        st.markdown("---")
        st.markdown("### 📖 Index Descriptions")
        
        with st.expander("ℹ️ What do these indices mean?"):
            st.markdown("""
            - **NDVI (Normalized Difference Vegetation Index)**: Measures vegetation greenness and health
            - **EVI (Enhanced Vegetation Index)**: Similar to NDVI but reduces atmospheric influences
            - **NDWI (Normalized Difference Water Index)**: Indicates vegetation water content
            - **SAVI (Soil Adjusted Vegetation Index)**: Minimizes soil brightness influences
            - **NBR (Normalized Burn Ratio)**: Useful for detecting burned areas
            - **BSI (Bare Soil Index)**: Indicates areas of exposed soil
            - **NDBI (Normalized Difference Built-up Index)**: Highlights built-up areas
            - **MNDWI (Modified NDWI)**: Enhanced water body detection
            """)
        
        # Map visualization
        st.markdown("---")
        st.markdown("### 🗺️ Spatial Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_index = st.selectbox(
                "Select index:",
                ['NDVI', 'EVI', 'NDWI', 'SAVI', 'NBR', 'BSI', 'NDBI', 'MNDWI']
            )
        
        with col2:
            selected_year = st.selectbox(
                "Select year:",
                analyzer.years,
                index=3
            )
        
        # Create map
        Map = geemap.Map(center=[-0.37, 35.28], zoom=10)
        
        # Add boundary
        Map.addLayer(analyzer.kericho, {}, 'Study Area', opacity=0.5)
        
        # Visualization parameters for each index
        vis_params_map = {
            'NDVI': {'min': -0.2, 'max': 0.8, 'palette': ['ff0000', 'ffff00', '00ff00']},
            'EVI': {'min': -0.2, 'max': 0.8, 'palette': ['8B4513', 'ffff00', '00ff00']},
            'NDWI': {'min': -0.5, 'max': 0.5, 'palette': ['8B4513', 'ffffff', '0000ff']},
            'SAVI': {'min': -0.2, 'max': 0.8, 'palette': ['ff0000', 'ffff00', '00ff00']},
            'NBR': {'min': -0.5, 'max': 0.5, 'palette': ['ff0000', 'ffff00', '00ff00']},
            'BSI': {'min': -1, 'max': 1, 'palette': ['00ff00', 'ffffff', '8B4513']},
            'NDBI': {'min': -1, 'max': 1, 'palette': ['00ff00', 'ffffff', '808080']},
            'MNDWI': {'min': -0.5, 'max': 0.5, 'palette': ['8B4513', 'ffffff', '0000ff']}
        }
        
        # Add index layer
        Map.addLayer(
            analyzer.indices[selected_year].select(selected_index),
            vis_params_map[selected_index],
            f'{selected_year} - {selected_index}'
        )
        
        Map.to_streamlit(height=600)
    
    
    # ═══════════════════════════════════════════════════════════════════
    # CLIMATE ANALYSIS
    # ═══════════════════════════════════════════════════════════════════
    
    elif analysis_mode == "🌤️ Climate Analysis":
        st.markdown("## 🌤️ Climate Trends Analysis")
        
        st.info("ℹ️ **Note:** Temperature data (MODIS) is only available from 2000 onwards. Years before 2000 show precipitation data only.")
        
        with st.spinner("Loading climate data..."):
            climate_data = analyzer.get_climate_trends()
        
        st.markdown("### 📋 Climate Data")
        st.dataframe(climate_data, use_container_width=True)
        
        # Download
        csv = climate_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Climate Data (CSV)",
            data=csv,
            file_name=f"kericho_climate_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Dual-axis chart
        st.markdown("### 📊 Temperature & Precipitation Trends")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Temperature
        fig.add_trace(
            go.Scatter(
                x=climate_data['Year'],
                y=climate_data['Temperature (°C)'],
                name="Temperature",
                line=dict(color='red', width=3),
                marker=dict(size=10)
            ),
            secondary_y=False
        )
        
        # Precipitation
        fig.add_trace(
            go.Scatter(
                x=climate_data['Year'],
                y=climate_data['Precipitation (mm)'],
                name="Precipitation",
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
        fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=True)
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Individual charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌡️ Temperature Trend")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=climate_data['Year'],
                y=climate_data['Temperature (°C)'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='red', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Temperature (°C)",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💧 Precipitation Trend")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=climate_data['Year'],
                y=climate_data['Precipitation (mm)'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Precipitation (mm)",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Map visualization
        st.markdown("---")
        st.markdown("### 🗺️ Spatial Climate Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            climate_var = st.selectbox(
                "Select variable:",
                ['Temperature', 'Precipitation']
            )
        
        with col2:
            climate_year = st.selectbox(
                "Select year:",
                analyzer.years,
                index=3,
                key='climate_year'
            )
        
        # Create map
        Map = geemap.Map(center=[-0.37, 35.28], zoom=10)
        
        # Add boundary
        Map.addLayer(analyzer.kericho, {}, 'Study Area', opacity=0.5)
        
        # Visualization parameters
        if climate_var == 'Temperature':
            vis_params = {'min': 15, 'max': 35, 'palette': ['0000ff', 'ffffff', 'ff0000']}
            band_name = 'temperature'
        else:
            vis_params = {'min': 800, 'max': 2000, 'palette': ['ffffff', '0000ff', '00008b']}
            band_name = 'precipitation'
        
        # Add climate layer
        Map.addLayer(
            analyzer.climate[climate_year].select(band_name),
            vis_params,
            f'{climate_year} - {climate_var}'
        )
        
        Map.to_streamlit(height=600)
    
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPREHENSIVE REPORT
    # ═══════════════════════════════════════════════════════════════════
    
    elif analysis_mode == "📋 Comprehensive Report":
        st.markdown("## 📋 Comprehensive Analysis Report")
        st.markdown(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        st.info("ℹ️ **Note:** Temperature data (MODIS) is only available from 2000 onwards.")
        
        with st.spinner("Generating comprehensive report..."):
            # Fetch all data
            lc_data = analyzer.calculate_land_cover_areas()
            veg_data = analyzer.get_vegetation_indices_trends()
            climate_data = analyzer.get_climate_trends()
            
            # Key changes
            change_1995_2024 = analyzer.calculate_change_matrix(1995, 2024)
        
        # Executive Summary
        st.markdown("### 📌 Executive Summary")
        
        latest = lc_data[lc_data['Year'] == 2024].iloc[0]
        first = lc_data[lc_data['Year'] == 1995].iloc[0]
        
        summary_text = f"""
        **Study Period:** 1995 - 2024 (30 years)
        
        **Study Area:** Kericho County, Kenya (~{sum([latest[c] for c in analyzer.class_names]):.0f} km²)
        
        **Key Findings:**
        
        - **Forest Cover:** {first['Forest']:.0f} km² (1995) → {latest['Forest']:.0f} km² (2024) 
          [Change: {((latest['Forest'] - first['Forest']) / first['Forest'] * 100):+.1f}%]
        
        - **Tea Plantations:** {first['Tea Plantations']:.0f} km² (1995) → {latest['Tea Plantations']:.0f} km² (2024) 
          [Change: {((latest['Tea Plantations'] - first['Tea Plantations']) / first['Tea Plantations'] * 100):+.1f}%]
        
        - **Built-up Areas:** {first['Built-up']:.0f} km² (1995) → {latest['Built-up']:.0f} km² (2024) 
          [Change: {((latest['Built-up'] - first['Built-up']) / first['Built-up'] * 100):+.1f}%]
        
        - **Mean NDVI (2024):** {veg_data[veg_data['Year'] == 2024]['NDVI'].values[0]:.3f}
        
        - **Mean Temperature (2024):** {climate_data[climate_data['Year'] == 2024]['Temperature (°C)'].values[0]:.1f}°C
        
        - **Annual Precipitation (2024):** {climate_data[climate_data['Year'] == 2024]['Precipitation (mm)'].values[0]:.0f} mm
        """
        
        st.info(summary_text)
        
        st.markdown("---")
        
        # Detailed sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Land Cover",
            "🔄 Changes",
            "🌿 Vegetation",
            "🌤️ Climate"
        ])
        
        with tab1:
            st.markdown("#### Land Cover Statistics")
            st.dataframe(lc_data, use_container_width=True)
            
            # Trend chart
            fig = go.Figure()
            for class_name in analyzer.class_names:
                fig.add_trace(go.Scatter(
                    x=lc_data['Year'],
                    y=lc_data[class_name],
                    mode='lines+markers',
                    name=class_name,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title="Land Cover Trends (1995-2024)",
                xaxis_title="Year",
                yaxis_title="Area (km²)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("#### Major Land Cover Changes (1995-2024)")
            
            if len(change_1995_2024) > 0:
                st.dataframe(change_1995_2024[['From', 'To', 'Area (km²)']], use_container_width=True)
                
                # Bar chart
                change_1995_2024['Transition'] = change_1995_2024['From'] + ' → ' + change_1995_2024['To']
                
                fig = go.Figure(go.Bar(
                    x=change_1995_2024['Area (km²)'],
                    y=change_1995_2024['Transition'],
                    orientation='h',
                    marker=dict(color='#2d5016')
                ))
                
                fig.update_layout(
                    title="Significant Transitions",
                    xaxis_title="Area (km²)",
                    height=max(300, len(change_1995_2024) * 40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant changes detected (>1 km²)")
        
        with tab3:
            st.markdown("#### Vegetation Index Trends")
            st.dataframe(veg_data, use_container_width=True)
            
            # Multi-line chart
            fig = go.Figure()
            for index in ['NDVI', 'EVI', 'NDWI']:
                fig.add_trace(go.Scatter(
                    x=veg_data['Year'],
                    y=veg_data[index],
                    mode='lines+markers',
                    name=index,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title="Key Vegetation Indices",
                xaxis_title="Year",
                yaxis_title="Index Value",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("#### Climate Trends")
            st.dataframe(climate_data, use_container_width=True)
            
            # Dual-axis chart
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(
                    x=climate_data['Year'],
                    y=climate_data['Temperature (°C)'],
                    name="Temperature",
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=climate_data['Year'],
                    y=climate_data['Precipitation (mm)'],
                    name="Precipitation",
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=True
            )
            
            fig.update_xaxes(title_text="Year")
            fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
            fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=True)
            
            fig.update_layout(
                title="Climate Variables Over Time",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Download all data
        st.markdown("### 📥 Export Report Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_lc = lc_data.to_csv(index=False)
            st.download_button(
                label="Land Cover Data",
                data=csv_lc,
                file_name=f"landcover_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            csv_veg = veg_data.to_csv(index=False)
            st.download_button(
                label="Vegetation Indices",
                data=csv_veg,
                file_name=f"vegetation_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col3:
            csv_climate = climate_data.to_csv(index=False)
            st.download_button(
                label="Climate Data",
                data=csv_climate,
                file_name=f"climate_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )


# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🌲 Kericho Forest Change Analysis Tool | Powered by Google Earth Engine</p>
        <p style='font-size: 0.9rem;'>Data Sources: Landsat 5/7/8/9, CHIRPS, MODIS | Analysis: Random Forest Classification</p>
    </div>
""", unsafe_allow_html=True)