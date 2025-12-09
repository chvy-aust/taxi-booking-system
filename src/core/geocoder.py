import json
import logging
from json import JSONDecodeError

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from src.utils.constants import ADDR_CACHE_FILE

logger = logging.getLogger(__name__)
class Geocoder:
    USER_AGENT = "CIS020-1_taxi_booking_app (contact: auschiel@gmail.com)"
    def __init__(self):
        self.service = Nominatim(user_agent=self.USER_AGENT)
        self.cache = self._load_cache() or None

    def get_coordinates(self, addr: str):
        """Return a resolved address + coords from provided addr."""
        normalized_addr = addr.lower().strip()
        if normalized_addr in self.cache:
            # lookup cache before querying
            return self.cache[normalized_addr]

        try:
            query = self.service.geocode(normalized_addr)
            if not query:
               return None

            coordinates = {
               "resolved_address": query.address,
               "lat": query.latitude,
               "long": query.longitude
            }
            json.dump(coordinates, ADDR_CACHE_FILE)
            return coordinates
        except (GeocoderServiceError, GeocoderTimedOut) as e:
            logger.exception(e)
            return None

    def get_address(self, coords: dict):
        """Return a resolved address from cords"""
        pass

    def _load_cache(self):
        try:
            with open(ADDR_CACHE_FILE, "r") as f:
                return json.load(f)
        except (OSError, JSONDecodeError) as e:
            logger.warning(f"Could not read address cache. Error: {e}")
            return None
