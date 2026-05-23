from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

import voluptuous as vol
import aiohttp
import async_timeout
import asyncio

from .const import DOMAIN, CONF_URL, CONF_TOKEN, CONF_PROJECT_ID


async def validate_connection(url: str, token: str) -> dict:
    """Testa la connessione reale a Semaphore UI."""

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    info_url = f"{url.rstrip('/')}/api/info"

    try:
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(info_url, headers=headers) as resp:

                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "success": True,
                            "version": data.get("version", "unknown")
                        }

                    elif resp.status in (401, 403):
                        return {
                            "success": False,
                            "error": "invalid_auth"
                        }

                    elif resp.status == 404:
                        return {
                            "success": False,
                            "error": "not_found"
                        }

                    return {
                        "success": False,
                        "error": f"http_error_{resp.status}"
                    }

    except (aiohttp.ClientError, asyncio.TimeoutError):
        return {
            "success": False,
            "error": "cannot_connect"
        }

    except Exception:
        return {
            "success": False,
            "error": "unknown"
        }


class SemaphoreConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow principale."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _build_schema(self, defaults=None):
        """Schema riutilizzabile."""

        defaults = defaults or {}

        return vol.Schema({
            vol.Required(
                CONF_URL,
                default=defaults.get(CONF_URL, "https://")
            ): str,

            vol.Required(
                CONF_TOKEN,
                default=defaults.get(CONF_TOKEN, "")
            ): str,

            vol.Required(
                CONF_PROJECT_ID,
                default=defaults.get(CONF_PROJECT_ID, 1)
            ): int,
        })

    def _build_errors(self, result):

        errors = {}

        if result["error"] == "invalid_auth":
            errors["token"] = "invalid_auth"

        elif result["error"] == "cannot_connect":
            errors["base"] = "cannot_connect"

        else:
            errors["base"] = "unknown"

        return errors

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Configurazione iniziale."""

        errors = {}

        if user_input is not None:

            result = await validate_connection(
                user_input[CONF_URL],
                user_input[CONF_TOKEN]
            )

            if result["success"]:
                return self.async_create_entry(
                    title="Semaphore UI",
                    data=user_input
                )

            errors = self._build_errors(result)

        return self.async_show_form(
            step_id="user",
            data_schema=self._build_schema(user_input),
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input=None
    ) -> FlowResult:
        """Gestisce il pulsante Riconfigura."""

        errors = {}

        entry = self._get_reconfigure_entry()

        if user_input is not None:

            result = await validate_connection(
                user_input[CONF_URL],
                user_input[CONF_TOKEN]
            )

            if result["success"]:

                self.hass.config_entries.async_update_entry(
                    entry,
                    data=user_input
                )

                await self.hass.config_entries.async_reload(
                    entry.entry_id
                )

                return self.async_abort(
                    reason="reconfigure_successful"
                )

            errors = self._build_errors(result)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self._build_schema(entry.data),
            errors=errors,
        )