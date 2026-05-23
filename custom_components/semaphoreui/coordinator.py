from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import aiohttp
import async_timeout
from datetime import timedelta
import logging

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class SemaphoreCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,                    # ← Questo mancava
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.entry = entry
        self.url = entry.data["url"].rstrip("/")
        self.token = entry.data["token"]
        self.project_id = entry.data.get("project_id", 1)

    async def _async_update_data(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

        try:
            async with async_timeout.timeout(20):
                connector = aiohttp.TCPConnector(ssl=False)  # puoi toglierlo dopo

                async with aiohttp.ClientSession(connector=connector) as session:
                    # Recupera i templates
                    templates_url = f"{self.url}/api/project/{self.project_id}/templates"
                    async with session.get(templates_url, headers=headers) as resp:
                        if resp.status != 200:
                            raise UpdateFailed(f"HTTP {resp.status}")
                        templates = await resp.json()

                    # Recupera le info generali (versione)
                    info_url = f"{self.url}/api/info"
                    async with session.get(info_url, headers=headers) as resp:
                        if resp.status == 200:
                            info = await resp.json()
                            version = info.get("version", "unknown")
                        else:
                            version = "unknown"

                    # Restituiamo un dizionario con entrambe le info
                    return {
                        "templates": templates,
                        "version": version
                    }

        except Exception as err:
            _LOGGER.error("Error fetching Semaphore data: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}")