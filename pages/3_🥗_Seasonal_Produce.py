import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    init_connection    
)

st.title("Seasonal Produce Explorer")

# Create tabs for different search methods
search_type = st.radio(
    "Search by:",
    ["Seasons", "Specific Produce"]
)

if search_type == "Seasons":
    # Multi-select for seasons
    seasons = ["spring", "summer", "fall", "winter", "year_round"]
    selected_seasons = st.multiselect(
        "Select season(s):",
        seasons,
        default=None
    )
    
    if selected_seasons:
        # Connect to MongoDB
        client = init_connection()
        db = client.food_database
        collection = db.seasonal_foods
        
        # Build the query based on selected seasons
        if "year_round" in selected_seasons:
            # Handle year-round separately
            other_seasons = [s for s in selected_seasons if s != "year_round"]
            if other_seasons:
                query = {
                    "$or": [
                        {"available_year_round": True},
                        {"seasons": {"$all": other_seasons}}  # Changed from $in to $all
                    ]
                }
        else:
            query = {"seasons": {"$all": selected_seasons}}
        
        # Execute query and display results
        results = list(collection.find(query).sort("name"))
        
        if results:
            st.subheader(f"Found {len(results)} items:")
            
            # Create columns for better organization
            col1, col2 = st.columns(2)
            
            # Split results between columns
            mid_point = len(results) // 2
            
            with col1:
                for item in results[:mid_point]:
                    seasons_text = ", ".join(item["seasons"])
                    if item.get("available_year_round"):
                        st.write(f"🟢 **{item['name']}** (Available year-round)")
                    else:
                        st.write(f"🔵 **{item['name']}** (Seasons: {seasons_text})")
            
            with col2:
                for item in results[mid_point:]:
                    seasons_text = ", ".join(item["seasons"])
                    if item.get("available_year_round"):
                        st.write(f"🟢 **{item['name']}** (Available year-round)")
                    else:
                        st.write(f"🔵 **{item['name']}** (Seasons: {seasons_text})")
        else:
            st.warning("No produce found for selected seasons.")

else:  # Specific Produce search
    client = init_connection()
    db = client.food_database
    collection = db.seasonal_foods
    
    all_produce = sorted([item["name"] for item in collection.find({}, {"name": 1})])
    
    selected_produce = st.selectbox(
        "Search for specific produce:",
        all_produce
    )
    
    if selected_produce:
        result = collection.find_one({"name": selected_produce})
        
        if result:
            st.subheader(f"Seasonal Availability for {result['name']}")
            
            if result.get("available_year_round"):
                st.success("✨ This produce is in season year-round!")
            else:
                seasons_text = ", ".join(result["seasons"])
                st.info(f"🗓️ Best seasons: {seasons_text}")
            
            # Create a visual representation of availability
            st.subheader("Availability Calendar")
            cols = st.columns(4)
            seasons_dict = {
                "spring": "🌱 Spring",
                "summer": "☀️ Summer",
                "fall": "🍂 Fall",
                "winter": "❄️ Winter"
            }
            
            for i, (season, label) in enumerate(seasons_dict.items()):
                with cols[i]:
                    if result.get("available_year_round") or season in result["seasons"]:
                        st.success(label)
                    else:
                        st.error(label)
        else:
            st.error("Produce not found in database.")
