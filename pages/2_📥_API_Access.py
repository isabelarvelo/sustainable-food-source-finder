import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    init_connection, 
    create_map, 
    get_food_sources,
    query_by_location,
    query_by_radius,
    query_by_products_and_location,
    query_seasonal_produce,
    query_location_density
)
import streamlit as st
import requests
import pandas as pd
from typing import Optional, Dict, Any
import json
from utils.api_utils import USDALocalFoodAPI, LocationQuery
import logging

def initialize_session_state():
    """Initialize session state variables."""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''

def save_api_key():
    """Save API key to session state."""
    st.session_state.api_key = st.session_state.api_key_input

def main():
    st.title("USDA Local Food Directory API Access")
    st.write("""
    Query the USDA Local Food Directory API directly to find farmers markets, CSAs, and on-farm markets 
    across the United States.
    """)
    
    st.write("You can query the USDA Local Food Directory API free of cost. In order to acquire an API key, visit the [API Documentation](https://www.ams.usda.gov/local-food-directories-api).")
    
    initialize_session_state()

    # API Key input
    api_key_input = st.text_input(
        "Enter your API Key",
        value=st.session_state.api_key,
        type="password",
        key="api_key_input",
        help="Enter your USDA Local Food Directory API key"
    )
    
    if st.button("Save API Key"):
        save_api_key()
        st.success("API Key saved successfully!")

    # Directory Selection
    directory = st.selectbox(
        "Select Directory Type",
        options=['farmers_market', 'csa', 'on_farm_market'],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Query Type Selection
    query_type = st.radio(
        "Select Query Type",
        [
            "State Search",
            "ZIP Code Search",
            "ZIP Code Radius Search",
            "Coordinate Search"
        ]
    )
    
    try:
        if st.session_state.api_key:
            api = USDALocalFoodAPI(api_key=st.session_state.api_key)
            
            if query_type == "State Search":
                state = st.text_input(
                    "State Abbreviation",
                    max_chars=2,
                    help="Enter two-letter state abbreviation (e.g., MI)"
                ).upper()
                
                if st.button("Search") and state:
                    with st.spinner("Searching..."):
                        results = api.search_by_state(directory, state)
                        
            elif query_type == "ZIP Code Search":
                zip = st.text_input(
                    "ZIP Code",
                    max_chars=5,
                    help="Enter 5-digit ZIP code"
                )
                
                if st.button("Search") and zip:
                    with st.spinner("Searching..."):
                        results = api.search_by_zip(directory, zip)
                        
            elif query_type == "ZIP Code Radius Search":
                col1, col2 = st.columns(2)
                with col1:
                    zip = st.text_input(
                        "ZIP Code",
                        max_chars=5,
                        help="Enter 5-digit ZIP code"
                    )
                with col2:
                    radius = st.slider(
                        "Radius (miles)",
                        min_value=1,
                        max_value=100,
                        value=25,
                        help="Maximum radius is 100 miles"
                    )
                
                if st.button("Search") and zip:
                    with st.spinner("Searching..."):
                        results = api.search_by_zip(directory, zip, radius)
                        
            elif query_type == "Coordinate Search":
                col1, col2 = st.columns(2)
                with col1:
                    latitude = st.number_input("Latitude", value=35.0)
                    longitude = st.number_input("Longitude", value=-85.0)
                with col2:
                    radius = st.slider(
                        "Radius (miles)",
                        min_value=1,
                        max_value=100,
                        value=25,
                        help="Maximum radius is 100 miles"
                    )
                
                if st.button("Search") and latitude and longitude:
                    with st.spinner("Searching..."):
                        results = api.search_by_coordinates(
                            directory, longitude, latitude, radius
                        )
            
            # Add in italics note about results
            st.write("*If there are no results for a zip code query, try using the zip code and radius option.")
            

            # Display results if they exist
            if 'results' in locals() and results:
                st.success(f"Found {len(results)} results!")
                
                # Display detailed results
                st.subheader("Detailed Results")
                for item in results:
                    with st.expander(
                        f"{item['listing_name']} ({item['location_city']}, {item['location_state']})"
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Location Details**")
                            st.write(f"Address: {item['location_address']}")
                            st.write(f"Type: {item['directory_name']}")
                            
                            if any([item['contact_name'], 
                                  item['contact_email'], 
                                  item['contact_phone']]):
                                st.write("**Contact Information**")
                                if item['contact_name']:
                                    st.write(f"Contact: {item['contact_name']}")
                                if item['contact_email']:
                                    st.write(f"Email: {item['contact_email']}")
                                if item['contact_phone']:
                                    st.write(f"Phone: {item['contact_phone']}")
                        
                        with col2:
                            if item['brief_desc']:
                                st.write("**Available Products**")
                                if 'Available Products:' in item['brief_desc']:
                                    products = item['brief_desc'].split('Available Products: ')[-1]
                                    for product in products.split(';'):
                                        if product.strip():
                                            st.write(f"- {product.strip()}")
                            
                            if any([item['media_website'], 
                                  item['media_facebook'], 
                                  item['media_twitter'], 
                                  item['media_instagram']]):
                                st.write("**Social Media**")
                                if item['media_website']:
                                    st.write(f"Website: {item['media_website']}")
                                if item['media_facebook']:
                                    st.write(f"Facebook: {item['media_facebook']}")
                                if item['media_twitter']:
                                    st.write(f"Twitter: {item['media_twitter']}")
                                if item['media_instagram']:
                                    st.write(f"Instagram: {item['media_instagram']}")
                                    
            elif 'results' in locals():
                st.warning("No results found for your search criteria.")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        logging.error(f"API Error: {str(e)}")

if __name__ == "__main__":
    main()