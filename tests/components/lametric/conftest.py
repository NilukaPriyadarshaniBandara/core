"""Fixtures for LaMetric integration tests."""
from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

from demetriek import CloudDevice, Device
from pydantic import parse_raw_as
import pytest

from homeassistant.components.application_credentials import (
    ClientCredential,
    async_import_client_credential,
)
from homeassistant.components.lametric.const import DOMAIN
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry, load_fixture


@pytest.fixture(autouse=True)
async def setup_credentials(hass: HomeAssistant) -> None:
    """Fixture to setup credentials."""
    assert await async_setup_component(hass, "application_credentials", {})
    await async_import_client_credential(
        hass, DOMAIN, ClientCredential("client", "secret"), "credentials"
    )


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="My LaMetric",
        domain=DOMAIN,
        data={
            CONF_HOST: "127.0.0.2",
            CONF_API_KEY: "mock-from-fixture",
            CONF_MAC: "AA:BB:CC:DD:EE:FF",
        },
        unique_id="SA110405124500W00BS9",
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Mock setting up a config entry."""
    with patch(
        "homeassistant.components.lametric.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_lametric_config_flow() -> Generator[MagicMock, None, None]:
    """Return a mocked LaMetric client."""
    with patch(
        "homeassistant.components.lametric.config_flow.LaMetricDevice", autospec=True
    ) as lametric_mock:
        lametric = lametric_mock.return_value
        lametric.api_key = "mock-api-key"
        lametric.host = "127.0.0.1"
        lametric.device.return_value = Device.parse_raw(
            load_fixture("device.json", DOMAIN)
        )
        yield lametric


@pytest.fixture
def mock_lametric_cloud_config_flow() -> Generator[MagicMock, None, None]:
    """Return a mocked LaMetric Cloud client."""
    with patch(
        "homeassistant.components.lametric.config_flow.LaMetricCloud", autospec=True
    ) as lametric_mock:
        lametric = lametric_mock.return_value
        lametric.devices.return_value = parse_raw_as(
            list[CloudDevice], load_fixture("cloud_devices.json", DOMAIN)
        )
        yield lametric


@pytest.fixture
def mock_lametric() -> Generator[MagicMock, None, None]:
    """Return a mocked LaMetric client."""
    with patch(
        "homeassistant.components.lametric.coordinator.LaMetricDevice", autospec=True
    ) as lametric_mock:
        lametric = lametric_mock.return_value
        lametric.api_key = "mock-api-key"
        lametric.host = "127.0.0.1"
        lametric.device.return_value = Device.parse_raw(
            load_fixture("device.json", DOMAIN)
        )
        yield lametric
