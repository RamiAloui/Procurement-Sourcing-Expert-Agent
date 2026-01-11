"""Shared test fixtures."""

import pytest

from src.config import DATA_PATH
from src.data.loader import DataLoader


@pytest.fixture
def data_loader():
    """Returns a DataLoader instance for testing."""
    return DataLoader(DATA_PATH)
