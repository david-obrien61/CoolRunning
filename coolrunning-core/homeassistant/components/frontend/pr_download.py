"""GitHub PR artifact download — disabled for standalone deployment."""

from __future__ import annotations

import pathlib

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


async def download_pr_artifact(
    hass: HomeAssistant,
    pr_number: int,
    github_token: str,
    tmp_dir: pathlib.Path,
) -> pathlib.Path:
    """Not available — GitHub integration disabled on standalone server."""
    raise HomeAssistantError(
        "Frontend PR download is disabled on standalone deployments."
    )
