from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN
from .coordinator import SemaphoreCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SemaphoreCoordinator = hass.data[DOMAIN][entry.entry_id]

    if not coordinator.data or not coordinator.data.get("templates"):
        return

    entities = []

    for template in coordinator.data["templates"]:
        template_id = template.get("id")
        name = template.get("name", "Unnamed Template")

        if template_id:
            entities.append(
                SemaphoreTemplateBinarySensor(
                    coordinator=coordinator,
                    template_id=template_id,
                    name=name,
                    entry=entry,
                )
            )

    async_add_entities(entities)


class SemaphoreTemplateBinarySensor(BinarySensorEntity):
    """Binary sensor for each Semaphore template."""

    def __init__(self, coordinator, template_id, name, entry):
        self.coordinator = coordinator
        self._template_id = template_id
        self._entry = entry

        self._attr_unique_id = f"semaphore_{template_id}"
        self._attr_name = f"{name}"
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self) -> bool | None:
        """True = Problem (rosso), False = OK"""
        data = self.coordinator.data
        if not data or not data.get("templates"):
            return None

        for t in data["templates"]:
            if t.get("id") == self._template_id:
                last_task = t.get("last_task")
                if last_task and last_task.get("status"):
                    return last_task.get("status") != "success"
                return True  # never run = problem
        return None

    @property
    def device_info(self):
        """Device principale"""
        version = self.coordinator.data.get("version", "unknown") if self.coordinator.data else "unknown"
        
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Semaphore UI",
            "manufacturer": "Semaphore",
            "model": f"Semaphore UI",
            "sw_version": version,
            "configuration_url": self._entry.data["url"],   # Link diretto
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )