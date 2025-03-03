# %%
import requests
import pandas as pd
import streamlit as st

# API sleutel
api_key = 'd5184c3b4e'

# Lijst van steden waarvoor je het weer wilt ophalen
cities = ['Voorhout', 'Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Alkmaar']

# Lijst voor het opslaan van de data van elke stad
weather_data = []

# Voor elke stad, haal het weer op via de API
for city in cities: 
    # API URL met de stadnaam als parameter
    api_url = f'https://weerlive.nl/api/weerlive_api_v2.php?key={api_key}&locatie={city}'

    # Maak de GET-aanroep naar de API
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            # Probeer de JSON te laden
            data = response.json()

            # Als de data de verwachte structuur heeft, verwerk het
            if isinstance(data, dict) and 'liveweer' in data:
                city_weather = data['liveweer']
                city_weather_df = pd.json_normalize(city_weather)

                # Voeg de stadnaam toe aan de data (optioneel, handig voor later)
                city_weather_df['stad'] = city

                # Voeg de data voor deze stad toe aan de lijst
                weather_data.append(city_weather_df)

            else:
                print(f"Data voor {city} niet gevonden in het verwachte formaat.")

        except ValueError as e:
            print(f"Fout bij het parseren van de JSON voor {city}: {e}")
    else:
        print(f"Fout bij ophalen van gegevens voor {city}: {response.status_code}")

# Combineer de gegevens van alle steden in één DataFrame
if weather_data:
    all_weather_data = pd.concat(weather_data, ignore_index=True)
    st.dataframe(all_weather_data)
else:
    print("Geen gegevens beschikbaar.")


