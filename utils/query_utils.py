from typing import Dict, List, Any, Optional
from datetime import datetime
import calendar


def query_by_location(collection, 
                     state: Optional[str] = None, 
                     city: Optional[str] = None, 
                     zipcode: Optional[str] = None) -> List[Dict]:
    """Search for food sources based on location parameters."""
    query = {}
    if state:
        query['location.state'] = state
    if city:
        query['location.city'] = city
    if zipcode:
        query['location.zipcode'] = zipcode
        
    return list(collection.find(query))

def query_by_radius(collection, 
                   longitude: float, 
                   latitude: float, 
                   radius_miles: float) -> List[Dict]:
    """Find food sources within a specified radius of coordinates."""
    radius_meters = radius_miles * 1609.34
    
    query = {
        'location.coordinates': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                '$maxDistance': radius_meters
            }
        }
    }
    
    return list(collection.find(query))

def query_by_products_and_location(collection,
                                 products: List[str],
                                 state: Optional[str] = None,
                                 city: Optional[str] = None) -> List[Dict]:
    """Search for food sources that have specific products available."""
    query = {
        'products.available_items': {
            '$in': products
        }
    }
    
    if state:
        query['location.state'] = state
    if city:
        query['location.city'] = city
        
    return list(collection.find(query))

def query_seasonal_produce(collection,
                         state: str,
                         month: int) -> Dict[str, List[str]]:
    """Find produce items that are in season for a given location and month."""
    pipeline = [
        {'$match': {
            'location.state': state,
            '$or': [
                {'products.seasonal': False},
                {
                    'products.seasonal': True,
                    'schedule.season_range.start_month': {'$lte': month},
                    'schedule.season_range.end_month': {'$gte': month}
                }
            ]
        }},
        {'$unwind': '$products.available_items'},
        {'$group': {
            '_id': None,
            'fresh_fruits': {
                '$addToSet': {
                    '$cond': [
                        {'$regexMatch': {
                            'input': '$products.available_items',
                            'regex': 'fruits?',
                            'options': 'i'
                        }},
                        '$products.available_items',
                        None
                    ]
                }
            },
            'fresh_vegetables': {
                '$addToSet': {
                    '$cond': [
                        {'$regexMatch': {
                            'input': '$products.available_items',
                            'regex': 'vegetables?',
                            'options': 'i'
                        }},
                        '$products.available_items',
                        None
                    ]
                }
            }
        }}
    ]
    
    result = list(collection.aggregate(pipeline))
    return result[0] if result else {'fresh_fruits': [], 'fresh_vegetables': []}

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
