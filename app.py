
import streamlit as st
import json
from datetime import date

DATA_FILE = "my_garden_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"zones": [], "plants": [], "observations_log": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def plant_form(data):
    st.header("Add a New Plant")
    name = st.text_input("Plant Name", key="plant_name")
    species = st.text_input("Species", key="species")
    plant_type = st.selectbox("Type", ["Perennial", "Annual", "Bulb"], key="plant_type")
    location_zone = st.selectbox("Location Zone", [z["zone_id"] for z in data["zones"]], key="location_zone")
    sun_exposure = st.selectbox("Sun Exposure", ["Full sun", "Partial shade", "Shade"], key="sun_exposure_plant")
    watering_needs = st.selectbox("Watering Needs", ["Light", "Medium", "Heavy"], key="watering_needs")
    fertilizer_type = st.text_input("Fertilizer Type", key="fertilizer_type")
    bloom_season = st.text_input("Bloom Season", key="bloom_season")
    last_watered = st.date_input("Last Watered", date.today(), key="last_watered")
    last_fertilized = st.date_input("Last Fertilized", date.today(), key="last_fertilized")

    if st.button("Add Plant", key="add_plant_button"):
        new_plant = {
            "name": name,
            "species": species,
            "type": plant_type,
            "location_zone": location_zone,
            "sun_exposure": sun_exposure,
            "watering_needs": watering_needs,
            "fertilizer_type": fertilizer_type,
            "bloom_season": bloom_season,
            "last_watered": str(last_watered),
            "last_fertilized": str(last_fertilized)
        }
        data["plants"].append(new_plant)
        save_data(data)
        st.success("Plant added!")

def zone_form(data):
    st.header("Add a New Garden Zone")
    zone_id = st.text_input("Zone ID", key="zone_id")
    description = st.text_input("Description", key="zone_description")
    sun_exposure = st.selectbox("Sun Exposure", ["Full sun", "Partial shade", "Shade"], key="sun_exposure_zone")
    soil_type = st.text_input("Soil Type", key="soil_type")
    pH = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1, key="ph")
    irrigated = st.checkbox("Irrigated", key="irrigated")

    if st.button("Add Zone", key="add_zone_button"):
        new_zone = {
            "zone_id": zone_id,
            "description": description,
            "sun_exposure": sun_exposure,
            "soil_type": soil_type,
            "pH": pH,
            "irrigated": irrigated
        }
        data["zones"].append(new_zone)
        save_data(data)
        st.success("Zone added!")

def observation_form(data):
    st.header("Log a Garden Observation")
    plant_name = st.selectbox("Plant Name", [p["name"] for p in data["plants"]], key="obs_plant_name")
    observation_type = st.selectbox("Observation Type", ["Watered", "Weeded", "Fertilized", "Pest Noted", "Other"], key="obs_type")
    notes = st.text_area("Notes", key="obs_notes")
    obs_date = st.date_input("Date", date.today(), key="obs_date")

    if st.button("Add Observation", key="add_obs_button"):
        new_obs = {
            "date": str(obs_date),
            "plant_name": plant_name,
            "observation_type": observation_type,
            "notes": notes
        }
        data["observations_log"].append(new_obs)
        save_data(data)
        st.success("Observation added!")

def main():
    st.title("My Garden Tracker")
    data = load_data()

    tab1, tab2, tab3 = st.tabs(["Add Plant", "Add Zone", "Log Observation"])

    with tab1:
        if data["zones"]:
            plant_form(data)
        else:
            st.warning("Please add at least one garden zone before adding plants.")

    with tab2:
        zone_form(data)

    with tab3:
        if data["plants"]:
            observation_form(data)
        else:
            st.warning("Please add at least one plant before logging observations.")

if __name__ == "__main__":
    main()
