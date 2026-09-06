"""Support for common values for MyHome devices."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gateway import MyHOMEGatewayHandler

from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_ENTITIES


from .const import DOMAIN, CONF_PLATFORMS, CONF_ENTITIES


class MyHOMEEntity(Entity):
    def __init__(
        self,
        hass,
        name: str,
        platform: str,
        device_id: str,
        who: str,
        where: str,
        manufacturer: str,
        model: str,
        gateway: MyHOMEGatewayHandler,
    ):
        self._hass = hass
        self._platform = platform
        self._who = who
        self._where = where
        self._device_id = device_id
        self._attr_unique_id = f"{gateway.mac}-{self._device_id}"
        self._manufacturer = manufacturer or "BTicino S.p.A."
        self._model = model
        self._gateway_handler = gateway
        self._attr_has_entity_name = True
        self._attr_name = None
        self._attr_entity_registry_enabled_default = True
        self._attr_should_poll = False

        from homeassistant.helpers import device_registry as dr

        dev_reg = dr.async_get(hass)
        gateway_device = dev_reg.async_get_device_by_identifier(
            DOMAIN, gateway.unique_id
        )

        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, f"{gateway.mac}-{self._device_id}")},
            name=name,
            manufacturer=self._manufacturer,
            model=self._model,
            via_device_id=gateway_device.id if gateway_device else None,
        )

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self._hass.data[DOMAIN][self._gateway_handler.mac][CONF_PLATFORMS][self._platform][self._device_id][CONF_ENTITIES][self._platform] = self
        await self.async_update()

    async def async_will_remove_from_hass(self):
        """When entity is removed from hass."""
        if self._platform in self._hass.data[DOMAIN][self._gateway_handler.mac][CONF_PLATFORMS][self._platform][self._device_id][CONF_ENTITIES]:
            del self._hass.data[DOMAIN][self._gateway_handler.mac][CONF_PLATFORMS][self._platform][self._device_id][CONF_ENTITIES][self._platform]
