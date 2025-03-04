import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--case_num", action="store_true", default="all", help="run tests api"
    )

@pytest.fixture(scope="session")
def get_case_num(pytestconfig):
    return pytestconfig.getoption("--case_num")