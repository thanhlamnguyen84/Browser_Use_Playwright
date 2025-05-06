# conftest.py
import pytest
def pytest_addoption(parser):
    parser.addoption(
        "--test_case",
        action="store",
        default="",
        help="Specify test case ID: iot_001 or iot_002. Leave empty to run all."
    )

@pytest.fixture
def test_case_option(request):
    return request.config.getoption("test_case")

