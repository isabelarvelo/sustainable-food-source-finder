import plotly.express as px
import pandas as pd
from typing import List, Dict

def create_map(data: List[Dict]):
    """
    Create the interactive map visualization with error handling for empty data.
    """
    # First create the locations data with better error handling
    locations = []
    for item in data:
        try:
            coordinates = item.get('location', {}).get('coordinates', {}).get('coordinates', [])
            if coordinates and len(coordinates) == 2:
                locations.append({
                    'name': item.get('listing_name', 'Unknown'),
                    'type': item.get('directory_type', 'Unknown'),
                    'lat': coordinates[1],
                    'lon': coordinates[0],
                    'address': item.get('location', {}).get('address', 'No address'),
                    'state': item.get('location', {}).get('state', '')
                })
        except (IndexError, TypeError):
            continue

    # If no valid locations found, create an empty map centered on the Southeast US
    if not locations:
        empty_df = pd.DataFrame({
            'lat': [35.0],
            'lon': [-85.0],
            'type': ['No results found'],
            'name': ['No results found'],
            'address': ['Try adjusting your filters']
        })
        
        fig = px.scatter_mapbox(
            empty_df,
            lat='lat',
            lon='lon',
            hover_name='name',
            mapbox_style='carto-positron'
        )
        
        fig.update_layout(
            title={
                'text': "No results found - Try adjusting your filters",
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 20}
            },
            mapbox=dict(
                center=dict(lat=35.0, lon=-85.0),
                zoom=5
            ),
            showlegend=False,
            margin={"r":0,"t":30,"l":0,"b":0},
            height=600
        )
        
        return fig

    # Create DataFrame from valid locations
    locations_df = pd.DataFrame(locations)

    # Create the map with the valid data
    fig = px.scatter_mapbox(
        locations_df,
        lat='lat',
        lon='lon',
        color='type',
        hover_name='name',
        hover_data={
            'type': True,
            'address': True
        },
        zoom=4,
        color_discrete_sequence=px.colors.qualitative.Set3,
        mapbox_style='carto-positron'
    )

    # Update layout
    fig.update_layout(
        title={
            'text': "Southeast U.S. Local Food Sources",
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        mapbox=dict(
            center=dict(lat=35.0, lon=-85.0),
            zoom=5
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        margin={"r":0,"t":30,"l":0,"b":0},
        height=600
    )

    return fig

