# %% [markdown]
# #Verwerken van API en downloaden van 

# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# %%
import requests
import pandas as pd

api_key = 'd5184c3b4e'
cities = [
    'Assen', 'Lelystad', 'Leeuwarden', 'Arnhem', 'Groningen', 'Maastricht', 
    'Eindhoven', 'Den Helder', 'Enschede', 'Amersfoort', 'Middelburg', 'Rotterdam'
]
liveweer = []
wk_verw = []
uur_verw = []
api_data = []

for city in cities:
    api_url = f'https://weerlive.nl/api/weerlive_api_v2.php?key={api_key}&locatie={city}'
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
        if 'api_data' in data:
            api_data.extend(data['api'])

    else:
        print(f"Error fetching data for {city}: {response.status_code}")

df_liveweer = pd.DataFrame(liveweer)
df_wk_verw = pd.DataFrame(wk_verw)
df_uur_verw = pd.DataFrame(uur_verw)
df_api_data = pd.DataFrame(api_data)
print(df_liveweer)


# %% [markdown]
# pd.DataFrame.from_dict(data)

# %%
# Save to CSV file
df_liveweer.to_csv('WL_LiveWeer.csv')
df_wk_verw.to_csv('WL_week_werwachting.csv')
df_uur_verw.to_csv('WL_uur_werwachting.csv')
df_api_data.to_csv('WL_API.csv')

# %% [markdown]
# Moet het volgende weten voordat ik verder kan:
# 1. Hoe kan ik locatie zetten bij uur- en weekverwachting? Kan ik 'plaats' van LiveWeer mergen met de andere twee DFs? (Done)

# %% [markdown]
# # Visualisaties #

# %%
import folium
import pandas as pd
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

# Add lat/lon to df_liveweer
df_liveweer["lat"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[0])
df_liveweer["lon"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[1])

# Create a folium map centered over the Netherlands
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

for index, row in df_liveweer.iterrows():
    weather_desc = row['samenv'].lower()
    icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
    icon_path = f"iconen-weerlive/{icon_file}"  # Folder path updated
    
    popup_text = f"{row['plaats']}: {row['temp']}°C, {row['samenv']}"
    
    # Add marker with the custom weather icon
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_text,
        tooltip=row["plaats"],
        icon=CustomIcon(icon_path, icon_size=(30, 30))
    ).add_to(nl_map)


# Display the map
nl_map


# %%
import folium
import pandas as pd
from folium.features import CustomIcon
from folium.plugins import TimestampedGeoJson
import json
from ipywidgets import interact

# City coordinates
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

# Reading CSV data (assuming df_uur_verw is already loaded with correct data)
df_uur_verw = pd.read_csv('WL_uur_werwachting.csv')

# Convert timestamps to datetime for easier manipulation
df_uur_verw['timestamp'] = pd.to_datetime(df_uur_verw['timestamp'], unit='s')

# Create the base map centered over the Netherlands
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

# Function to update markers for a given hour
def update_map(hour):
    # Clear current markers
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    
    # Filter data for the given hour
    hour_data = df_uur_verw[df_uur_verw['timestamp'].dt.hour == hour]
    
    for index, row in hour_data.iterrows():
        weather_desc = row['image'].lower()
        icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
        icon_path = f"iconen-weerlive/{icon_file}"  # Folder path
        
        popup_text = f"{row['plaats']}: {row['temp']}°C, {row['image']}"
        
        # Add marker with the custom weather icon
        folium.Marker(
            location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
            popup=popup_text,
            tooltip=row["plaats"],
            icon=CustomIcon(icon_path, icon_size=(30, 30))
        ).add_to(nl_map)
    
    return nl_map

# Create an interactive slider using ipywidgets
interact(update_map, hour=(0, 23, 1));


# %%
import folium
import pandas as pd
from folium.features import CustomIcon
from ipywidgets import interact, Dropdown
import os

# City coordinates
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

# Reading CSV data (assuming df_uur_verw is already loaded with correct data)
df_uur_verw = pd.read_csv('WL_uur_werwachting.csv')

# Convert timestamps to datetime for easier manipulation
df_uur_verw['timestamp'] = pd.to_datetime(df_uur_verw['timestamp'], unit='s')

# Create the base map centered over the Netherlands
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

# Function to update markers for a given hour and parameter (neersl, temp, or image)
def update_map(hour, parameter):
    # Clear current markers
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    
    # Filter data for the given hour
    hour_data = df_uur_verw[df_uur_verw['timestamp'].dt.hour == hour]
    
    for index, row in hour_data.iterrows():
        weather_desc = row['image'].lower()  # Default to 'image' for icon
        icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
        icon_path = f"iconen-weerlive/{icon_file}"  # Folder path
        
        # Determine popup text based on selected parameter
        if parameter == "temp":
            popup_text = f"{row['plaats']}: {row['temp']}°C"
        elif parameter == "image":
            popup_text = f"{row['plaats']}: {row['image']}"
        elif parameter == "neersl":
            popup_text = f"{row['plaats']}: {row['neersl']} mm"
        
        # Add marker with the custom weather icon
        folium.Marker(
            location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
            popup=popup_text,
            tooltip=row["plaats"],
            icon=CustomIcon(icon_path, icon_size=(30, 30))
        ).add_to(nl_map)
    
    return nl_map

# Create an interactive dropdown and slider
def interactive_map(hour, parameter):
    return update_map(hour, parameter)

parameter_dropdown = Dropdown(
    options=["temp", "image", "neersl"],
    value="temp",  # Default value
    description="Parameter:",
    disabled=False
)

# Display the slider and dropdown for interaction
interact(interactive_map, hour=(0, 23, 1), parameter=parameter_dropdown);


# %%


# %%
import folium
import pandas as pd
from folium.features import CustomIcon
from ipywidgets import interact, Dropdown
import os

# City coordinates
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

# Reading CSV data (assuming df_uur_verw is already loaded with correct data)
df_uur_verw = pd.read_csv('WL_uur_werwachting.csv')

# Convert timestamps to datetime for easier manipulation
df_uur_verw['timestamp'] = pd.to_datetime(df_uur_verw['timestamp'], unit='s')

# Create the base map centered over the Netherlands
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

# Function to update markers for a given hour and parameter (neersl, temp, or image)
def update_map(hour, parameter):
    # Clear current markers
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    
    # Filter data for the given hour
    hour_data = df_uur_verw[df_uur_verw['timestamp'].dt.hour == hour]
    
    for index, row in hour_data.iterrows():
        weather_desc = row['image'].lower()  # Default to 'image' for icon
        icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
        icon_path = f"iconen-weerlive/{icon_file}"  # Folder path
        
        # Determine popup text based on selected parameter
        if parameter == "temp":
            popup_text = f"{row['plaats']}: {row['temp']}°C"  # Show temperature directly, no image
        elif parameter == "neersl":
            popup_text = f"{row['plaats']}: {row['neersl']} mm"  # Show precipitation in mm, no image
        elif parameter == "image":
            popup_text = f"{row['plaats']}: {row['image']}"  # Show weather description and image
        
        # Add marker with the custom weather icon
        if parameter == "image":
            # Only when 'image' is selected, add the icon
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=CustomIcon(icon_path, icon_size=(30, 30))
            ).add_to(nl_map)
        else:
            # When 'temp' or 'neersl' is selected, don't add an image, just show the text
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"]
            ).add_to(nl_map)
    
    return nl_map

# Create an interactive dropdown and slider
def interactive_map(hour, parameter):
    return update_map(hour, parameter)

# Create the dropdown for selecting parameter
parameter_dropdown = Dropdown(
    options=["temp", "image", "neersl"],
    value="temp",  # Default value
    description="Parameter:",
    disabled=False
)

# Display the slider and dropdown for interaction
interact(interactive_map, hour=(0, 23, 1), parameter=parameter_dropdown);


# %%


# %%
import folium
import pandas as pd
from folium.features import CustomIcon, DivIcon
from ipywidgets import interact, Dropdown

# City coordinates
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

# Reading CSV data (assuming df_uur_verw is already loaded with correct data)
df_uur_verw = pd.read_csv('WL_uur_werwachting.csv')

# Convert timestamps to datetime for easier manipulation
df_uur_verw['timestamp'] = pd.to_datetime(df_uur_verw['timestamp'], unit='s')

# Create the base map centered over the Netherlands
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

# Function to update markers for a given hour and parameter (neersl, temp, or image)
def update_map(hour, parameter):
    # Clear current markers
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    
    # Filter data for the given hour
    hour_data = df_uur_verw[df_uur_verw['timestamp'].dt.hour == hour]
    
    for index, row in hour_data.iterrows():
        # Select the value based on the parameter
        if parameter == "temp":
            popup_text = f"{row['plaats']}: {row['temp']}°C"  # Show temperature directly
            value = f"{row['temp']}°C"  # Number for temperature with unit
        elif parameter == "neersl":
            popup_text = f"{row['plaats']}: {row['neersl']} mm"  # Show precipitation in mm
            value = f"{row['neersl']} mm"  # Number for precipitation with unit
        elif parameter == "image":
            weather_desc = row['image'].lower()  # Default to 'image' for icon
            icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
            icon_path = f"iconen-weerlive/{icon_file}"  # Folder path
            popup_text = f"{row['plaats']}: {row['image']}"  # Show weather description
            value = None  # No number, just show icon for image
        
        # Add the city number using DivIcon when temp or neersl is selected
        if value is not None:
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=DivIcon(
                    icon_size=(30, 30),
                    icon_anchor=(15, 15),
                    html=f'<div style="font-size: 14px; color: black; font-weight: bold;">{value}</div>'  # Display number with unit
                )
            ).add_to(nl_map)
        # Add the weather icon when image is selected
        elif parameter == "image":
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=CustomIcon(icon_path, icon_size=(30, 30))  # Show image icon
            ).add_to(nl_map)
    
    return nl_map

# Create an interactive dropdown and slider
def interactive_map(hour, parameter):
    return update_map(hour, parameter)

# Create the dropdown for selecting parameter
parameter_dropdown = Dropdown(
    options=["temp", "image", "neersl"],
    value="temp",  # Default value
    description="Parameter:",
    disabled=False
)

# Display the slider and dropdown for interaction
interact(interactive_map, hour=(0, 23, 1), parameter=parameter_dropdown);


# %%
import folium
import pandas as pd
from folium.features import CustomIcon, DivIcon
from ipywidgets import interact, Dropdown, Checkbox, VBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
from PIL import Image
from IPython.display import display

# City coordinates
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

# Reading CSV data (assuming df_uur_verw is already loaded with correct data)
df_uur_verw = pd.read_csv('WL_uur_werwachting.csv')

# Convert timestamps to datetime for easier manipulation
df_uur_verw['timestamp'] = pd.to_datetime(df_uur_verw['timestamp'], unit='s')

# Function to update markers for a given hour and parameter (neersl, temp, or image)
def update_map(hour, parameter):
    # Create the base map centered over the Netherlands
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    
    # Filter data for the given hour
    hour_data = df_uur_verw[df_uur_verw['timestamp'].dt.hour == hour]
    
    for index, row in hour_data.iterrows():
        # Select the value based on the parameter
        if parameter == "temp":
            popup_text = f"{row['plaats']}: {row['temp']}°C"  # Show temperature directly
            value = f"{row['temp']}°C"  # Number for temperature with unit
        elif parameter == "neersl":
            popup_text = f"{row['plaats']}: {row['neersl']} mm"  # Show precipitation in mm
            value = f"{row['neersl']} mm"  # Number for precipitation with unit
        elif parameter == "image":
            weather_desc = row['image'].lower()  # Default to 'image' for icon
            icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default to "bewolkt.png" if no match
            icon_path = f"iconen-weerlive/{icon_file}"  # Folder path
            popup_text = f"{row['plaats']}: {row['image']}"  # Show weather description
            value = None  # No number, just show icon for image
        
        # Add the city number using DivIcon when temp or neersl is selected
        if value is not None:
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=DivIcon(
                    icon_size=(30, 30),
                    icon_anchor=(15, 15),
                    html=f'<div style="font-size: 14px; color: black; font-weight: bold;">{value}</div>'  # Display number with unit
                )
            ).add_to(nl_map)
        # Add the weather icon when image is selected
        elif parameter == "image":
            folium.Marker(
                location=[city_coords[row["plaats"]][0], city_coords[row["plaats"]][1]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=CustomIcon(icon_path, icon_size=(30, 30))  # Show image icon
            ).add_to(nl_map)
    
    return nl_map

# Function to plot the graph for a selected city or all cities and parameter
def plot_graph(parameter, city="All Cities"):
    # Filter data for the selected city
    if city == "All Cities":
        city_data = df_uur_verw
    else:
        city_data = df_uur_verw[df_uur_verw['plaats'] == city]
    
    # Plot based on selected parameter
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if parameter == "temp":
        for city_name in city_data['plaats'].unique():
            city_specific_data = city_data[city_data['plaats'] == city_name]
            ax.plot(city_specific_data['timestamp'], city_specific_data['temp'], label=f'Temperature for {city_name}')
        ax.set_ylabel('Temperature (°C)')
    elif parameter == "neersl":
        for city_name in city_data['plaats'].unique():
            city_specific_data = city_data[city_data['plaats'] == city_name]
            ax.plot(city_specific_data['timestamp'], city_specific_data['neersl'], label=f'Precipitation for {city_name}')
        ax.set_ylabel('Precipitation (mm)')
    elif parameter == "image":
        # We cannot plot images, but we can show the number of occurrences of each image per city
        image_counts = city_data['image'].value_counts()
        ax.bar(image_counts.index, image_counts.values, color='skyblue')
        ax.set_ylabel('Occurrences of Weather Image')
    
    ax.set_title(f"{parameter.capitalize()} Data ({city})")
    ax.set_xlabel('Time')
    ax.set_xticklabels(city_data['timestamp'], rotation=45)
    ax.legend()
    
    # Save the plot to a PNG image in memory
    canvas = FigureCanvas(fig)
    img_buffer = io.BytesIO()
    canvas.print_png(img_buffer)
    img_buffer.seek(0)
    
    # Convert to an Image object for embedding in folium
    img = Image.open(img_buffer)
    img_path = "/tmp/graph.png"
    img.save(img_path)
    
    return img_path

# Create an interactive dropdown and slider
def interactive_map(hour, parameter, city, show_graph):
    # Update the map with selected parameters
    nl_map = update_map(hour, parameter)
    
    # If the checkbox for showing the graph is selected, overlay the graph on the map
    if show_graph:
        img_path = plot_graph(parameter, city)
        
        # Add the graph image as an overlay on the map
        folium.raster_layers.ImageOverlay(
            name="Graph Overlay",
            image=img_path,
            bounds=[[52.0, 4.0], [53.5, 7.5]],  # Coordinates to place the image over the map
            opacity=0.7,
            interactive=True,
            cross_origin=False,
        ).add_to(nl_map)
    
    return nl_map

# Create the dropdown for selecting parameter
parameter_dropdown = Dropdown(
    options=["temp", "image", "neersl"],
    value="temp",  # Default value
    description="Parameter:",
    disabled=False
)

# Create the checkbox for selecting city
city_checkbox = Checkbox(
    value=False,
    description='Show Graph for Selected City',
)

# Create a dropdown for selecting the city
city_dropdown = Dropdown(
    options=["All Cities"] + list(df_uur_verw['plaats'].unique()),  # Add "All Cities" option
    description="City:",
    disabled=False
)

# Display the slider, dropdown for parameter, and city selection
VBox([parameter_dropdown, city_checkbox, city_dropdown])
interact(interactive_map, hour=(0, 23, 1), parameter=parameter_dropdown, city=city_dropdown, show_graph=city_checkbox);


# %%


# %%



