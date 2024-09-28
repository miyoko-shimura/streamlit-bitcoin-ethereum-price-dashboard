import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Built-in data for major world cities
cities_data = {
    'name': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Moscow', 'Beijing', 'Rio de Janeiro', 'Cairo', 'Mumbai'],
    'latitude': [40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 55.7558, 39.9042, -22.9068, 30.0444, 19.0760],
    'longitude': [-74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 37.6173, 116.4074, -43.1729, 31.2357, 72.8777],
    'population': [8419000, 8982000, 37400000, 2161000, 5312000, 12506000, 21540000, 6320000, 20076000, 20411000]
}

st.title('Easy Geo Visualization App')

# Create DataFrame and GeoDataFrame
df = pd.DataFrame(cities_data)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326")

# Create a world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Visualization options
st.sidebar.header('Visualization Options')
show_labels = st.sidebar.checkbox('Show City Names', value=True)
marker_size = st.sidebar.slider('Marker Size', min_value=10, max_value=300, value=100)
color_by = st.sidebar.selectbox('Color by', ['Uniform', 'Population'])

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
world.plot(ax=ax, color='lightgrey', edgecolor='black')

if color_by == 'Uniform':
    gdf.plot(ax=ax, color='red', markersize=marker_size)
else:
    gdf.plot(ax=ax, column='population', cmap='viridis', markersize=marker_size, legend=True, legend_kwds={'label': 'Population', 'orientation': 'horizontal'})

if show_labels:
    for idx, row in gdf.iterrows():
        ax.annotate(row['name'], xy=(row['longitude'], row['latitude']), xytext=(3, 3), 
                    textcoords="offset points", fontsize=8)

plt.title('Major World Cities')
st.pyplot(fig)

# Display the data
st.subheader('City Data:')
st.write(df)

# Add some information about the app
st.sidebar.markdown("""
## About this app

This app visualizes the locations of major world cities on a map. 
You can customize the visualization using the options above.

- Toggle city name labels
- Adjust the size of the markers
- Color the markers uniformly or by population

The data table below the map shows detailed information about each city.
""")
