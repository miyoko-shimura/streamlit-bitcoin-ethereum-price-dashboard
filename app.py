import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Built-in data for major world cities
cities_data = {
    'name': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Moscow', 'Beijing', 'Rio de Janeiro', 'Cairo', 'Mumbai'],
    'latitude': [40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 55.7558, 39.9042, -22.9068, 30.0444, 19.0760],
    'longitude': [-74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 37.6173, 116.4074, -43.1729, 31.2357, 72.8777],
    'population': [8419000, 8982000, 37400000, 2161000, 5312000, 12506000, 21540000, 6320000, 20076000, 20411000]
}

st.title('Simple Geo Visualization App')

# Create DataFrame
df = pd.DataFrame(cities_data)

# Visualization options
st.sidebar.header('Visualization Options')
show_labels = st.sidebar.checkbox('Show City Names', value=True)
marker_size = st.sidebar.slider('Marker Size', min_value=10, max_value=300, value=100)
color_by = st.sidebar.selectbox('Color by', ['Uniform', 'Population'])

# Plot
fig, ax = plt.subplots(figsize=(12, 8))

# Create a simple world map (rectangle)
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
ax.set_facecolor('lightblue')

# Plot cities
if color_by == 'Uniform':
    ax.scatter(df['longitude'], df['latitude'], s=marker_size, color='red')
else:
    scatter = ax.scatter(df['longitude'], df['latitude'], s=marker_size, c=df['population'], cmap='viridis')
    plt.colorbar(scatter, label='Population', orientation='horizontal', pad=0.08)

if show_labels:
    for _, row in df.iterrows():
        ax.annotate(row['name'], (row['longitude'], row['latitude']), xytext=(3, 3), 
                    textcoords="offset points", fontsize=8)

plt.title('Major World Cities')
st.pyplot(fig)

# Display the data
st.subheader('City Data:')
st.write(df)

# Add some information about the app
st.sidebar.markdown("""
## About this app

This app visualizes the locations of major world cities on a simple world map. 
You can customize the visualization using the options above.

- Toggle city name labels
- Adjust the size of the markers
- Color the markers uniformly or by population

The data table below the map shows detailed information about each city.
""")
