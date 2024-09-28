import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Built-in data for major world cities
cities_data = {
    'name': ['ニューヨーク', 'ロンドン', '東京', 'パリ', 'シドニー', 'モスクワ', '北京', 'リオデジャネイロ', 'カイロ', 'ムンバイ'],
    'latitude': [40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 55.7558, 39.9042, -22.9068, 30.0444, 19.0760],
    'longitude': [-74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 37.6173, 116.4074, -43.1729, 31.2357, 72.8777],
    'population': [8419000, 8982000, 37400000, 2161000, 5312000, 12506000, 21540000, 6320000, 20076000, 20411000]
}

st.title('世界の主要都市ビジュアライゼーション')

# Create DataFrame
df = pd.DataFrame(cities_data)

# Visualization options
st.sidebar.header('表示オプション')
show_labels = st.sidebar.checkbox('都市名を表示', value=True)
marker_size = st.sidebar.slider('マーカーサイズ', min_value=10, max_value=300, value=100)
color_by = st.sidebar.selectbox('色分け', ['単色', '人口'])

# Plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Plot cities
if color_by == '単色':
    ax.scatter(df['longitude'], df['latitude'], s=marker_size, color='red', transform=ccrs.PlateCarree())
else:
    scatter = ax.scatter(df['longitude'], df['latitude'], s=marker_size, c=df['population'], 
                         cmap='viridis', transform=ccrs.PlateCarree())
    plt.colorbar(scatter, label='人口', orientation='horizontal', pad=0.08)

if show_labels:
    for _, row in df.iterrows():
        ax.text(row['longitude'], row['latitude'], row['name'], fontsize=8, 
                ha='right', va='bottom', transform=ccrs.PlateCarree())

ax.set_global()
plt.title('世界の主要都市')
st.pyplot(fig)

# Display the data
st.subheader('都市データ:')
st.write(df)

# Add some information about the app
st.sidebar.markdown("""
## このアプリについて

このアプリは世界の主要都市の位置を世界地図上に表示します。
上記のオプションを使用して、表示をカスタマイズできます。

- 都市名ラベルの表示/非表示
- マーカーサイズの調整
- 単色または人口に基づく色分け

地図の下のデータテーブルには、各都市の詳細情報が表示されます。
""")
