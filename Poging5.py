# %%
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from folium.features import CustomIcon

# City coordinations for icon placements
city_coords = {
    "Assen": [52.9929, 6.5642],
    "Lelystad": [52.5185, 5.4714],
    "Leeuwarden": [53.2012, 5.7999],
    "Arnhem": [51.9851, 5.8987],
    "Groningen": [53.2194, 6.5665],
    "Maastricht": [50.8514, 5.6910],
    "Eindhoven": [51.4416, 5.4697],
    "Den Helder": [52.9563, 4.7601],
    "Enschede": [52.2215, 6.8937],
    "Amersfoort": [52.1561, 5.3878],
    "Middelburg": [51.4988, 3.6136],
    "Rotterdam": [51.9225, 4.4792],
}

# Weather condition to icon mapping
weather_icons = {
    "zonnig": "zonnig.png",
    "bewolkt": "bewolkt.png",
    "half bewolkt": "halfbewolkt.png",
    "licht bewolkt": "halfbewolkt.png",
    "regen": "regen.png",
    "buien": "buien.png",
    "mist": "mist.png",
    "sneeuw": "sneeuw.png",
    "onweer": "bliksem.png",
    "hagel": "hagel.png",
    "heldere nacht": "helderenacht.png",
    "nachtmist": "nachtmist.png",
    "wolkennacht": "wolkennacht.png",
    "zwaar bewolkt": "zwaarbewolkt.png"
}

# Voeg lat/lon toe aan df_liveweer
df_liveweer["lat"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[0])
df_liveweer["lon"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[1])

# Voeg lat/lon toe aan df_uur_verw (weersvoorspelling per uur)
df_uur_verw["lat"] = df_uur_verw["plaats"].map(lambda city: city_coords.get(city, [None, None])[0])
df_uur_verw["lon"] = df_uur_verw["plaats"].map(lambda city: city_coords.get(city, [None, None])[1])

# Zorg ervoor dat de kolom met uren numeriek is
df_uur_verw["uur"] = pd.to_numeric(df_uur_verw["uur"], errors="coerce")

# Streamlit titel
st.title("Weerkaart van Nederland met Uur Slider")

# **1. Creëer de slider** voor de beschikbare uren
min_uur = int(df_uur_verw["uur"].min())
max_uur = int(df_uur_verw["uur"].max())
selected_uur = st.slider("Selecteer een uur:", min_uur, max_uur, min_uur)

# **2. Filter df_uur_verw** op basis van de gekozen uurwaarde
df_filtered = df_uur_verw[df_uur_verw["uur"] == selected_uur]

# **3. Creëer een folium kaart**
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

for _, row in df_filtered.iterrows():
    weather_desc = row['samenv'].lower()
    icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default naar "bewolkt.png"
    icon_path = f"iconen-weerlive/{icon_file}"  # Dit pad blijft ongewijzigd zoals je wilde

    popup_text = f"{row['plaats']}: {row['temp']}°C, {row['samenv']} ({selected_uur}:00)"

    # Voeg marker toe met weericoon
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_text,
        tooltip=row["plaats"],
        icon=CustomIcon(icon_path, icon_size=(30, 30))
    ).add_to(nl_map)

# **4. Toon de kaart in Streamlit**
st_folium(nl_map, width=700, height=500)


