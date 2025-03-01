import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--api", action="store_true", default="tc", help="run tests api"
    )

@pytest.fixture(scope="session")
def get_api(pytestconfig):
    return pytestconfig.getoption("--api")