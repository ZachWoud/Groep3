import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.features import CustomIcon

# ---- 📌 API Configuration ----
API_KEY = 'd5184c3b4e'
CITIES = [
    'Assen', 'Lelystad', 'Leeuwarden', 'Arnhem', 'Groningen', 'Maastricht', 
    'Eindhoven', 'Den Helder', 'Enschede', 'Amersfoort', 'Middelburg', 'Rotterdam'
]

# ---- 📌 City Coordinates ----
CITY_COORDS = {
    "Assen": [52.9929, 6.5642], "Lelystad": [52.5185, 5.4714], "Leeuwarden": [53.2012, 5.7999],
    "Arnhem": [51.9851, 5.8987], "Groningen": [53.2194, 6.5665], "Maastricht": [50.8514, 5.6910],
    "Eindhoven": [51.4416, 5.4697], "Den Helder": [52.9563, 4.7601], "Enschede": [52.2215, 6.8937],
    "Amersfoort": [52.1561, 5.3878], "Middelburg": [51.4988, 3.6136], "Rotterdam": [51.9225, 4.4792]
}

# ---- 📌 Weather Icons ----
WEATHER_ICONS = {
    "zonnig": "zonnig.png", "bewolkt": "bewolkt.png", "half bewolkt": "halfbewolkt.png",
    "licht bewolkt": "halfbewolkt.png", "regen": "regen.png", "buien": "buien.png",
    "mist": "mist.png", "sneeuw": "sneeuw.png", "onweer": "bliksem.png", "hagel": "hagel.png",
    "heldere nacht": "helderenacht.png", "nachtmist": "nachtmist.png", "wolkennacht": "wolkennacht.png",
    "zwaar bewolkt": "zwaarbewolkt.png"
}

# ---- 📌 Function: Fetch Weather Data ----
def fetch_weather_data():
    """Fetches live weather data for the configured cities."""
    liveweer, wk_verw, uur_verw = [], [], []

    for city in CITIES:
        api_url = f'https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={city}'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if 'liveweer' in data:
                liveweer.extend(data['liveweer'])
            if 'wk_verw' in data:
                for entry in data['wk_verw']:
                    entry['plaats'] = city
                wk_verw.extend(data['wk_verw'])
            if 'uur_verw' in data:
                for entry in data['uur_verw']:
                    entry['plaats'] = city
                uur_verw.extend(data['uur_verw'])
        else:
            st.warning(f"Error fetching data for {city}: {response.status_code}")

    return pd.DataFrame(liveweer), pd.DataFrame(wk_verw), pd.DataFrame(uur_verw)

# ---- 📌 Fetch Data Once ----
df_liveweer, df_wk_verw, df_uur_verw = fetch_weather_data()

# ---- 📌 Ensure Data Consistency ----
for df in [df_liveweer, df_uur_verw]:
    df["lat"] = df["plaats"].map(lambda city: CITY_COORDS.get(city, [None, None])[0])
    df["lon"] = df["plaats"].map(lambda city: CITY_COORDS.get(city, [None, None])[1])

df_uur_verw["uur"] = pd.to_numeric(df_uur_verw["uur"], errors="coerce")
df_uur_verw.dropna(subset=["uur"], inplace=True)
df_uur_verw["uur"] = df_uur_verw["uur"].astype(int)

# ---- 📌 Streamlit UI ----
st.title("📍 Weerkaart van Nederland")

# ---- 📌 Hour Selection Slider ----
if df_uur_verw.empty:
    st.error("⚠ Geen weergegevens beschikbaar.")
    df_filtered = pd.DataFrame()  # Define an empty DataFrame to avoid NameError
else:
    min_uur, max_uur = df_uur_verw["uur"].min(), df_uur_verw["uur"].max()
    selected_uur = st.slider("⏳ Selecteer een uur:", min_uur, max_uur, min_uur)
    df_filtered = df_uur_verw[df_uur_verw["uur"] == selected_uur]

# ---- 📌 Function: Create Map ----
def create_weather_map(df):
    """Creates a Folium map with weather markers."""
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

    for _, row in df.iterrows():
        weather_desc = row['samenv'].lower()
        icon_file = WEATHER_ICONS.get(weather_desc, "bewolkt.png")
        icon_path = f"iconen-weerlive/{icon_file}"  # Path unchanged

        popup_text = f"{row['plaats']}: {row['temp']}°C, {row['samenv']} ({selected_uur}:00)"

        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_text,
            tooltip=row["plaats"],
            icon=CustomIcon(icon_path, icon_size=(30, 30))
        ).add_to(nl_map)

    return nl_map

# ---- 📌 Display Map in Streamlit ----
if not df_filtered.empty:
    st_folium(create_weather_map(df_filtered), width=700, height=500)
else:
    st.warning("Geen gegevens om weer te geven op de kaart.")
