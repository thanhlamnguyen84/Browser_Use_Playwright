# conftest.py

import pytest
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from agent_browser.agents import *

# Initialize browser context and all agents at runtime
browser_context = BrowserContext(BrowserContextConfig())
login_agent, iot_001, iot_002, tear_down = get_agents(browser_context)

# ✅ Add custom command-line option
def pytest_addoption(parser):
    parser.addoption(
        "--test_case",
        action="store",
        default="",
        help="Test case to run: iot_001, iot_002. Leave empty to run all."
    )

# ✅ Retrieve the CLI option in test functions
@pytest.fixture
def test_case_option(request):
    return request.config.getoption("test_case")

# ✅ Setup and teardown logic for all tests
@pytest.fixture(scope="session", autouse=True)
async def setup_teardown():
    print("➡ Running login_agent")
    await login_agent.run()

    yield  # --- Test runs here ---

    print("⬅ Running tear_down")
    await tear_down.run()
    await browser_context.close()
    from browser_use.browser.browser import browser  # Delayed import if needed
    await browser.close()
