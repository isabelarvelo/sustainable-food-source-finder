from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, List
import requests
import logging
import time
from urllib.parse import urlencode

@dataclass
class LocationQuery:
    """Container for location-based query parameters."""
    state: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    radius: Optional[int] = None

    def validate(self) -> bool:
        """Validate location query parameters."""
        # Must have at least one location parameter
        if not any([self.state, self.zip_code, self.city, self.coordinates]):
            return False

        # City must have state
        if self.city and not self.state:
            return False

        # Radius must be positive and <= 100 if provided
        if self.radius is not None and (self.radius <= 0 or self.radius > 100):
            return False

        return True

    def to_params(self) -> Dict[str, Any]:
        """Convert to API parameters."""
        params = {}
        if self.zip_code:
            params['zip'] = self.zip_code
        if self.state:
            params['state'] = self.state
        if self.coordinates:
            params['x'] = self.coordinates[0]
            params['y'] = self.coordinates[1]
        if self.radius:
            params['radius'] = self.radius
        return params

class USDALocalFoodAPI:
    """Client for interacting with USDA Local Food Directory APIs."""
    
    BASE_URL = "https://www.usdalocalfoodportal.com/api"
    DIRECTORIES = {
        'csa': 'csa',
        'farmers_market': 'farmersmarket',
        'on_farm_market': 'onfarmmarket'
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.google.com/"
        }

    def _build_url(self, directory: str, params: Dict[str, Any]) -> str:
        """Build the API URL for a specific directory with API key first."""
        if directory not in self.DIRECTORIES:
            raise ValueError(f"Invalid directory. Must be one of: {', '.join(self.DIRECTORIES.keys())}")
        
        # Ensure API key is first by creating ordered params
        ordered_params = {'apikey': self.api_key}
        ordered_params.update(params)
        
        base = f"{self.BASE_URL}/{self.DIRECTORIES[directory]}/"
        return f"{base}?{urlencode(ordered_params)}"

    def fetch_listings(self, 
                      directory: str, 
                      location: LocationQuery,
                      max_retries: int = 5) -> List[Dict[str, Any]]:
        """Fetch listings from a specific directory using location parameters."""
        if not location.validate():
            raise ValueError("Invalid location query parameters")

        params = location.to_params()
        url = self._build_url(directory, params)
        
        print("URL: ", url)
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=20
                )
                
                if response.status_code == 200:
                    return response.json().get('data', [])
                    
                elif response.status_code == 429:
                    wait_time = min(2 ** attempt, 60)
                    logging.warning(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    logging.error(f"API request failed: {response.status_code}")
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    logging.error(f"Failed to fetch data after {max_retries} attempts: {str(e)}")
                    raise
                continue

        return []
    
    def search_by_state(self, directory: str, state: str) -> List[Dict[str, Any]]:
        """Search listings by state."""
        query = LocationQuery(state=state)
        return self.fetch_listings(directory, query)

    def search_by_zip(self, 
                     directory: str, 
                     zip_code: str, 
                     radius: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search listings by ZIP code with optional radius."""
        if radius is not None:
            query = LocationQuery(zip_code=zip_code, radius=radius)
        else:
            query = LocationQuery(zip_code=zip_code)
        return self.fetch_listings(directory, query)
        
    def search_by_coordinates(self, 
                            directory: str, 
                            longitude: float, 
                            latitude: float, 
                            radius: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search listings by coordinates with optional radius."""
        query = LocationQuery(coordinates=(longitude, latitude), radius=radius)
        return self.fetch_listings(directory, query)