"""
Test configuration for pytest-docker integration.

This module configures pytest-docker to use the main docker-compose.yml file
instead of a test-specific one, enabling unified build and test setup.
"""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def tjbots_env_file(pytestconfig):
    """Point TJBots to use the staging env file for tests.

    This ensures PackageConfig loads keys from ``env/staging.env`` by default.
    """
    root = str(pytestconfig.rootdir)
    staging_env_path = os.path.join(root, "env", "staging.env")
    os.environ.setdefault("TJBOTS_ENV_FILE", staging_env_path)


@pytest.fixture(scope="session", autouse=True)
def docker_compose_env(pytestconfig):
    """Set environment variables required by the main docker-compose.yml file."""
    # Set default values for testing
    test_env = {
        "DOCKER_NAME": "tjbots",
        "DOCKER_IMG": "tjbots",
        "VERSION": "test",
        "SECRETS_FILE": os.path.join(str(pytestconfig.rootdir), "env", "test.env")
    }

    for key, value in test_env.items():
        os.environ.setdefault(key, value)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Override the default docker-compose file location."""
    return os.path.join(str(pytestconfig.rootdir), "build", "docker-compose.yml")
