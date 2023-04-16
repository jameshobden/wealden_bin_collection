import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wealden_bin_collection"
PLATFORMS = ["sensor"]

CONF_UPRN = "uprn"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_UPRN): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Wealden Bin Collection component."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    uprn = conf.get(CONF_UPRN)
    hass.data[DOMAIN] = {CONF_UPRN: uprn}

    for platform in PLATFORMS:
        hass.async_create_task(async_load_platform(hass, platform, DOMAIN, {}, config))

    return True