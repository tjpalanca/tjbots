import pytest


@pytest.fixture(scope="session")
def docker_cleanup() -> bool:
    return False
