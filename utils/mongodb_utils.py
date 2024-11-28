# utils/mongodb_utils.py
import pymongo
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional

@st.cache_resource
def init_connection():
    """Initialize MongoDB connection."""
    print("Initializing MongoDB connection...")
    client = pymongo.MongoClient(**st.secrets["mongo"])
    print(f"Connected to MongoDB at {st.secrets['mongo']['host']}")
    return client

def ensure_geospatial_index(collection):
    """Ensure the necessary geospatial index exists."""
    collection.create_index([('location.coordinates', pymongo.GEOSPHERE)])

def get_food_sources(_client, filters=None):
    """Get food sources from MongoDB with optional filters."""
    print("\nFetching food sources from MongoDB...")
    print(f"Applied filters: {filters}")
    
    db = _client.sustainable_food_db
    collection = db.food_sources
    
    query = {}
    if filters:
        for key, value in filters.items():
            if value:
                if key == 'state':
                    query['location.state'] = value
                elif key == 'source_type':
                    query['directory_type'] = value
                elif key == 'products':
                    query['products.available_items'] = {'$in': [value]}
    
    results = list(collection.find(query))
    return results

def query_location_density(collection, state: str) -> Dict[str, Any]:
    # Get the state's area from states collection
    client = collection.database.client
    states_collection = client.us_geography.states_area
    state_data = states_collection.find_one({"state": state})
    
    if not state_data:
        return None
    
    # Query food sources in the state
    sources = list(collection.find({"location.state": state}))
    
    if not sources:
        return None
    
    # Calculate density using land area (converting from square km to square miles if needed)
    land_area = state_data["LandArea"]  # Assuming this is in square miles
    num_sources = len(sources)
    
    # Get unique types of sources
    source_types = list(set(source["directory_type"] for source in sources if "directory_type" in source))
    
    return {
        "state": state,
        "total_sources": num_sources,
        "land_area_sq_miles": land_area,
        "density_per_sq_mile": num_sources / land_area,
        "types": source_types
    }