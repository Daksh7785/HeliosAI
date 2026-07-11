import pytest

@pytest.fixture
def sample_flare_data():
    """
    Returns synthetic flare event data for testing.
    """
    return {"class": "M", "peak_flux": 1e-5}
