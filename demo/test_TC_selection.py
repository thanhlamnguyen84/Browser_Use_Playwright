# testcases/test_TC_selection.py

import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.browser.browser import Browser, BrowserConfig
from agents import get_agents

browser_context_config = BrowserContextConfig(
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1450, 'height': 700},
    locale='vi-VN',
    highlight_elements=True,
    # viewport_expansion=0
    # save_recording_path=os.path.join(project_root, 'exports', 'recordings'),
    # trace_path=os.path.join(project_root, 'exports', 'traces')
)
# Create BrowserConfig of Browser Use provided
browser_config = BrowserConfig(
    headless=False,
    disable_security=True
    # chrome_instance_path=r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # chrome_instance_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)
browser = Browser(config=browser_config)
browser_context = BrowserContext(
    browser= browser,
    config=browser_context_config

)

# Initialize browser context and agents
# browser_context = BrowserContext(browser_context_config)
login_agent, iot_001, iot_002, tear_down = get_agents(browser_context)


# Login and teardown fixture
# @pytest.fixture(scope="session", autouse=True)
# async def setup_teardown():
#     print("➡ Login agent setup")
#     await login_agent.run()
#     yield
#     print("⬅ Running tear down")
#     await tear_down.run()
#     await browser_context.close()
#     await browser.close()

# Test runner

@pytest.mark.asyncio
async def test_case_dispatcher(test_case_option):
    print(f"📌 test_case = '{test_case_option or '[empty]'}'")

    print("➡ Setup (login_agent)")
    await login_agent.run()

    try:
        if test_case_option == "iot_001":
            print("▶ Running iot_001")
            await iot_001.run()

        elif test_case_option == "iot_002":
            print("▶ Running iot_002")
            await iot_002.run()

        elif test_case_option == "":
            print("⚠ No test_case specified → Running all cases")
            print("▶ Running iot_001")
            await iot_001.run()
            print("▶ Running iot_002")
            await iot_002.run()
        else:
            pytest.skip(f"❌ Invalid test_case ID: {test_case_option}")

    finally:
        print("⬅ Teardown (tear_down)")
        await tear_down.run()
        await browser_context.close()
        await browser.close()

