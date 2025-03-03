import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--case_num", action="store_true", default="all", help="run tests api"
    )

@pytest.fixture(scope="session")
def get_api(pytestconfig):
    return pytestconfig.getoption("--case_num")