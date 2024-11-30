import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    init_connection, 
    create_map, 
    query_by_location,
    query_by_radius,
    query_by_products_and_location,
    query_location_density, 
    
)
import calendar

def query_by_zip(collection, zip_code: str):
    """Query food sources by zip code"""
    return list(collection.find({'location.zipcode': zip_code}))

def main():
    st.title("Southeast US Food Source Queries")
    st.write("Explore detailed data about sustainable food sources in the Southeast United States")
    
    # Initialize connection
    client = init_connection()
    db = client.sustainable_food_db
    collection = db.food_sources
    
    # Create query type selector
    query_type = st.radio(
        "Select Query Type",
        [
            "Location-based Search",
            "Radius Search",
            "Product Search",
            "Source Density Analysis"
        ]
    )
    
    # Container for results
    results_container = st.container()
    
    if query_type == "Location-based Search":
        st.subheader("Search by Location")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            state = st.selectbox(
                "Select State",
                ["All"] + sorted(list(set(
                    item['location']['state'] 
                    for item in collection.find({}, {'location.state': 1})
                    if item.get('location', {}).get('state')
                )))
            )
        
        with col2:
            cities = ["All"]
            if state != "All":
                cities.extend(sorted(list(set(
                    item['location']['city']
                    for item in collection.find({'location.state': state}, {'location.city': 1})
                    if item.get('location', {}).get('city')
                ))))
            city = st.selectbox("Select City", cities)
        
        with col3:
            source_type = st.selectbox(
                "Source Type",
                ["All"] + sorted(list(set(
                    item['directory_type']
                    for item in collection.find({}, {'directory_type': 1})
                )))
            )
        
        if st.button("Search"):
            query_params = {}
            if state != "All":
                query_params['state'] = state
            if city != "All":
                query_params['city'] = city
            
            results = query_by_location(collection, **query_params)
            
    elif query_type == "Radius Search":
        st.subheader("Search by Distance")
        st.info("Enter coordinates and radius to find nearby food sources")
        
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=35.0)
            longitude = st.number_input("Longitude", value=-85.0)
        
        with col2:
            radius = st.slider("Search Radius (miles)", 1, 100, 25)
        
        if st.button("Search"):
            results = query_by_radius(collection, longitude, latitude, radius)
            
    elif query_type == "Product Search":
        st.subheader("Search by Products")
        
        col1, col2 = st.columns(2)
        with col1:
            state = st.selectbox(
                "Select State (Optional)",
                ["All"] + sorted(list(set(
                    item['location']['state']
                    for item in collection.find({}, {'location.state': 1})
                    if item.get('location', {}).get('state')
                )))
            )
        
        with col2:
            all_products = sorted(list(set(
                product
                for item in collection.find({}, {'products.available_items': 1})
                for product in item.get('products', {}).get('available_items', [])
            )))
            
            selected_products = st.multiselect(
                "Select Products",
                all_products
            )
        
        if st.button("Search"):
            query_params = {
                'products': selected_products
            }
            if state != "All":
                query_params['state'] = state
            results = query_by_products_and_location(collection, **query_params)
     
    elif query_type == "Source Density Analysis":
        st.subheader("Analyze Source Density")
        
        state = st.selectbox(
            "Select State",
            sorted(list(set(
                item['location']['state']
                for item in collection.find({}, {'location.state': 1})
                if item.get('location', {}).get('state')
            )))
        )
        
        if st.button("Analyze"):
            density_results = query_location_density(collection, state)
            
            if density_results:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Food Sources per Square Mile",
                        f"{density_results['density_per_sq_mile']:.3f}"
                    )
                    st.metric(
                        "Total Food Sources",
                        density_results['total_sources']
                    )
                
                with col2:
                    st.metric(
                        "Land Area (sq miles)",
                        f"{density_results['land_area_sq_miles']:,.0f}"
                    )
                
                st.write("**Types of Sources Found:**")
                for source_type in density_results['types']:
                    st.write(f"- {source_type}")
            else:
                st.error("No data available for selected state.")
    
    # Display results if available
    if 'results' in locals():
        with results_container:
            st.subheader(f"Found {len(results)} matches")
            
            # Create and display map
            fig = create_map(results)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display results
            for item in results:
                with st.expander(f"{item['listing_name']} ({item['location']['city']}, {item['location']['state']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Location Details**")
                        st.write(f"Address: {item['location']['address']}")
                        st.write(f"Type: {item['directory_type']}")
                        
                        if any(item['contact'].values()):
                            st.write("**Contact Information**")
                            if item['contact']['name']:
                                st.write(f"Name: {item['contact']['name']}")
                            if item['contact']['email']:
                                st.write(f"Email: {item['contact']['email']}")
                            if item['contact']['phone']:
                                st.write(f"Phone: {item['contact']['phone']}")
                    
                    with col2:
                        if item['products']['available_items']:
                            st.write("**Available Products**")
                            st.write(", ".join(item['products']['available_items']))
                        
                        if any(item['media'].values()):
                            st.write("**Social Media**")
                            for platform, url in item['media'].items():
                                if url:
                                    st.write(f"{platform}: {url}")

if __name__ == "__main__":
    main()