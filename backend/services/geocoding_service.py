import logging
import time
from functools import lru_cache
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OpenCageService:
    """OpenCage Geocoding API service with retry, timeout, and caching"""
    
    def __init__(self, api_key: str):
        """
        Initialize OpenCage service
        
        Args:
            api_key (str): OpenCage API key
        """
        self.api_key = api_key
        self.base_url = "https://api.opencagedata.com/geocode/v1/json"
        self.timeout = 10  # 10 seconds timeout
        self.max_retries = 2
        self.min_confidence = 7  # Minimum confidence score
        
    @lru_cache(maxsize=500)
    def geocode(self, location: str) -> Dict[str, Any]:
        """
        Geocode a location using OpenCage API with retry logic and caching
        
        Args:
            location (str): Location string to geocode
            
        Returns:
            Dict[str, Any]: Geocoding result with lat, lon, formatted, confidence
            
        Raises:
            ValueError: If geocoding fails or confidence is too low
        """
        if not location or not location.strip():
            raise ValueError("Location cannot be empty")
            
        location = location.strip()
        
        # Try geocoding with retry logic
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = self._make_request(location)
                return result
                
            except requests.exceptions.Timeout as e:
                last_error = f"Request timeout: {e}"
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s
                    logger.warning(f"Timeout on attempt {attempt + 1}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                last_error = f"Request failed: {e}"
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    logger.warning(f"Request failed on attempt {attempt + 1}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                last_error = f"Unexpected error: {e}"
                # Don't retry on unexpected errors
                break
        
        # If we get here, all retries failed
        logger.error(f"Geocoding failed after {self.max_retries + 1} attempts for location: {location}")
        raise ValueError(last_error)
    
    def _make_request(self, location: str) -> Dict[str, Any]:
        """Make the actual API request"""
        params = {
            'q': location,
            'key': self.api_key,
            'language': 'vi',  # Vietnamese language for better results
            'limit': 10  # Get multiple results to choose best
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            # Handle HTTP errors
            if response.status_code == 401:
                raise ValueError("Invalid OpenCage API key")
            elif response.status_code == 402:
                raise ValueError("OpenCage API quota exceeded")
            elif response.status_code == 429:
                raise ValueError("OpenCage API rate limit exceeded")
            elif response.status_code == 500:
                raise ValueError("OpenCage API server error")
            elif response.status_code != 200:
                raise ValueError(f"OpenCage API error: HTTP {response.status_code}")
            
            data = response.json()
            
            # Check if we got results
            if not data.get('results'):
                raise ValueError("No results found for location")
            
            # Find best result based on confidence
            best_result = self._find_best_result(data['results'])
            
            if best_result is None:
                raise ValueError(f"No results with sufficient confidence (min: {self.min_confidence})")
            
            return best_result
            
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.RequestException as e:
            raise
        except ValueError as e:
            # Re-raise JSON decode errors
            raise
        except Exception as e:
            raise ValueError(f"Failed to parse OpenCage response: {e}")
    
    def _find_best_result(self, results: list) -> Optional[Dict[str, Any]]:
        """Find the best result based on confidence score"""
        best_result = None
        best_confidence = 0
        
        for result in results:
            # Extract confidence from annotations if available
            confidence = self._extract_confidence(result)
            
            # Skip results with low confidence
            if confidence < self.min_confidence:
                continue
                
            # Prefer higher confidence
            if confidence > best_confidence:
                best_confidence = confidence
                best_result = {
                    'lat': result['geometry']['lat'],
                    'lon': result['geometry']['lng'],
                    'formatted': result['formatted'],
                    'confidence': confidence
                }
        
        return best_result
    
    def _extract_confidence(self, result: Dict[str, Any]) -> float:
        """Extract confidence score from result"""
        # OpenCage provides confidence in annotations
        annotations = result.get('annotations', {})
        
        # Try different confidence indicators
        if 'confidence' in annotations:
            return annotations['confidence']
        elif 'wikidata' in annotations and annotations['wikidata']:
            # If we have wikidata, it's usually reliable
            return 9.0
        elif 'place_type' in result:
            # Different place types have different reliability
            place_type = result['place_type']
            type_confidence = {
                'building': 9.0,
                'house': 9.0,
                'address': 8.0,
                'street': 7.0,
                'city': 6.0,
                'town': 6.0,
                'village': 5.0,
                'country': 4.0
            }
            return type_confidence.get(place_type, 5.0)
        
        # Default confidence
        return 5.0


class GeocodingService:
    """Legacy geocoding service for backward compatibility"""
    
    def __init__(self):
        pass
    
    def geocode(self, location: str) -> tuple:
        """
        Legacy geocoding method that returns tuple format
        
        Args:
            location (str): Location to geocode
            
        Returns:
            tuple: (lat, lon, addr) or (None, None, None) if failed
        """
        # This is the old method that should be replaced
        # For now, return None values to indicate failure
        logger.warning("Legacy GeocodingService.geocode() called - this should be replaced with OpenCageService")
        return None, None, None