
import streamlit as st
import pandas as pd
import folium

# Load Airbnb dataset
@st.cache_data  # Cache the data to avoid reloading on every interaction
def load_data():
    return pd.read_csv('AB_US_2023.csv')  # Replace with your dataset's filename

# Create a map
def create_map(df, city):
    city_df = df[df['city'] == city]
    city_df = city_df.head(1000)
    city_map = folium.Map(location=[city_df['latitude'].mean(), city_df['longitude'].mean()], zoom_start=13)

    for index, row in city_df.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(city_map)

    return city_map

def main():
    st.title('Airbnb Room Prices and Listings Map')

    # Load the data
    df = load_data()

    # Create a dropdown to select the city
    cities = df['city'].unique()
    selected_city = st.selectbox('Select a city:', cities)

    # Filter data based on selected city
    filtered_data = df[df['city'] == selected_city]

    # Calculate average room prices for each room type
    avg_prices = filtered_data.groupby('room_type')['price'].mean()

    # Display average room prices in a table
    st.subheader('Average Room Prices')
    st.table(avg_prices)

    # Display the map using st.components.v1.html
    st.subheader('Listings Map')
    city_map = create_map(filtered_data, selected_city)
    city_map.save('city_map.html')

    # Specify encoding as 'utf-8'
    with open('city_map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=500)

if __name__ == "__main__":
    main()
