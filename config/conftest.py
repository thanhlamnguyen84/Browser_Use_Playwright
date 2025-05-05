# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--test_case",
        action="store",
        default="",
        help="Test case to run: iot_001, iot_002. Leave empty to run all."
    )

@pytest.fixture
def test_case_option(request):
    return request.config.getoption("--test_case")

# Async setup/teardown logic (auto-injected in every test session)
@pytest.fixture(scope="session", autouse=True)
async def setup_teardown():
    print("➡ Running login_agent...")
    await login_agent.run()
    yield
    print("⬅ Running tear_down...")
    await tear_down.run()
    await browser_context.close()
    await browser.close()
