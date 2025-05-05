# testcases/test_selection.py

import pytest
from agent_browser.agents import get_agents
from browser_use.browser.context import BrowserContext, BrowserContextConfig

# Initialize agents using the same context used in conftest.py
browser_context = BrowserContext(BrowserContextConfig())
_, iot_001, iot_002, _ = get_agents(browser_context)  # login_agent and tear_down are managed by conftest.py

@pytest.mark.asyncio
async def test_selected_case(test_case_option):
    if test_case_option == "iot_001":
        print("➡ Running test case: iot_001")
        await iot_001.run()
    elif test_case_option == "iot_002":
        print("➡ Running test case: iot_002")
        await iot_002.run()
    else:
        print("⚠ No valid test case specified. Running all...")
        print("➡ Running iot_001")
        await iot_001.run()
        print("➡ Running iot_002")
        await iot_002.run()
