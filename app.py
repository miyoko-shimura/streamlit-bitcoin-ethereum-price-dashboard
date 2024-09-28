import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Load population data (you would replace this with your actual data source)
population_data = pd.DataFrame({
    'country': ['United States', 'China', 'India', 'Brazil', 'Russia', 'Indonesia', 'Pakistan', 'Nigeria', 'Bangladesh', 'Mexico'],
    'population': [331002651, 1439323776, 1380004385, 212559417, 145934462, 273523615, 220892340, 206139589, 164689383, 128932753],
    'area_km2': [9833517, 9596961, 3287263, 8515767, 17098246, 1904569, 881912, 923768, 147570, 1964375]
})

# Calculate population density
population_data['density'] = population_data['population'] / population_data['area_km2']

# Merge with world map data
world = world.merge(population_data, how='left', left_on=['name'], right_on=['country'])

# Streamlit app
st.title('World Population Density Visualization')

# Create a choropleth map
st.subheader('1. World Population Density Map')
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(column='density', ax=ax, legend=True,
           legend_kwds={'label': 'Population Density (people/km²)', 'orientation': 'horizontal'},
           missing_kwds={'color': 'lightgrey'})
ax.set_axis_off()
st.pyplot(fig)

# Bar chart
st.subheader('2. Population by Country')
fig, ax = plt.subplots(figsize=(12, 6))
population_data.sort_values('population', ascending=False).plot(x='country', y='population', kind='bar', ax=ax)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Population')
st.pyplot(fig)

# Scatter plot
st.subheader('3. Population vs Area')
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=population_data, x='area_km2', y='population', hue='country', ax=ax)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Area (km²)')
plt.ylabel('Population')
st.pyplot(fig)

# Pie chart
st.subheader('4. Population Distribution')
fig, ax = plt.subplots(figsize=(12, 8))
population_data.plot.pie(y='population', labels=population_data['country'], autopct='%1.1f%%', ax=ax)
plt.ylabel('')
st.pyplot(fig)

# Histogram
st.subheader('5. Distribution of Population Density')
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(data=population_data, x='density', bins=20, kde=True, ax=ax)
plt.xlabel('Population Density (people/km²)')
st.pyplot(fig)

# Display data table
st.subheader('Population Density Data')
st.dataframe(population_data)

# Allow users to add new country data
st.subheader('Add New Country Data')
new_country = st.text_input('Country Name')
new_population = st.number_input('Population', min_value=0)
new_area = st.number_input('Area (km²)', min_value=0.0)

if st.button('Add Country'):
    new_density = new_population / new_area if new_area > 0 else 0
    new_data = pd.DataFrame({
        'country': [new_country],
        'population': [new_population],
        'area_km2': [new_area],
        'density': [new_density]
    })
    population_data = pd.concat([population_data, new_data], ignore_index=True)
    st.success(f'Added {new_country} to the dataset!')
    st.dataframe(population_data)
