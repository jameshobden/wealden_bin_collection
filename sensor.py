import logging
import requests
from datetime import datetime

from homeassistant.helpers.entity import Entity

from . import DOMAIN, CONF_UPRN

_LOGGER = logging.getLogger(__name__)

RESOURCE = "http://MYLOCALURL.com" # Use a local proxy url to avoid scraping the council website

COLLECTION_TYPES = {
    "black": "Black Bin Collection Date",
    "green": "Green Bin Collection Date",
    "brown": "Brown Bin Collection Date"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Wealden Bin Collection platform."""
    uprn = hass.data[DOMAIN].get(CONF_UPRN)

    if not uprn:
        _LOGGER.error("UPRN is not configured.")
        return

    sensors = [WealdenBinCollectionSensor(uprn, collection_type, name)
               for collection_type, name in COLLECTION_TYPES.items()]

    add_entities(sensors, True)


class WealdenBinCollectionSensor(Entity):
    """Representation of a Wealden Bin Collection sensor."""

    def __init__(self, uprn, collection_type, name, icon="mdi:trash-can"):
        """Initialize the Wealden Bin Collection sensor."""
        self._uprn = uprn
        self._collection_type = collection_type
        self._name = name
        self._icon = icon
        self._state = None

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return f"wealden_{self._collection_type}_collection"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        response = requests.get(RESOURCE, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                collection = data.get("collection")
                if collection:
                    collection_date = self._get_collection_date(collection)
                    if collection_date:
                        self._state = collection_date.strftime("%d/%m/%Y")
                else:
                    _LOGGER.error("Error retrieving collection data: No collection found")
            else:
                _LOGGER.error("Error: %s", data.get("message"))
        else:
            _LOGGER.error("Unable to fetch data from Wealden Council API. Status Code: %s", response.status_code)

    def _get_collection_date(self, collection):
        """Return the collection date based on the collection type."""
        try:
            if self._collection_type == "black":
                return datetime.fromisoformat(collection.get("refuseCollectionDate"))
            if self._collection_type == "green":
                return datetime.fromisoformat(collection.get("recyclingCollectionDate"))
            if self._collection_type == "brown":
                return datetime.fromisoformat(collection.get("gardenCollectionDate"))
        except KeyError as e:
            _LOGGER.error("KeyError: %s", e)
            return None
