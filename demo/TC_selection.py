import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use import Agent
from playwright.async_api import expect
from config.credentials import *
from config.config import *


login = (
f"Open Web '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}' to login"
)

# Create agent_browser with the model and browser context
login_agent = Agent(
    task=login,
    llm=llm,
    browser_context=browser_context

	)

iot_001 = Agent(
    task=(
        "click 'Add Chart' button"
        "Select Energy Consumption and click Next"
        "Click Select Sensors > input 'Active power - Phase A' in search box"
        "Select checkbox in search result list > click Add button"
        "In chart name column, input 'iot_001chart'"
        "Click create button"
        "Verify the text '1/1 chart(s) are successfully created...' is displays"
        "Click OK and stay there in 10 seconds"
        "Verify that the chart with name 'iot_001chart' displayed in Dashboard"
    ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)
iot_002 = Agent(
    task=(
        "click 'Add Chart' button"
        "Select Water Consumption and click Next"
        "Click Select Sensors"
        "Select a checkbox > click Add button"
        "In chart name column, input 'iot_002chart'"
        "Click create button"
        "Click OK and stay there in 10 seconds"
        "Verify that the chart with name 'iot_002chart' displayed in Dashboard"
    ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)

tear_down = Agent(
    task=(
        "Find all the chart with name 'iot001chart' and 'iot002chart' delete them"
    ),
    llm = llm,
    browser_context = browser_context
    # validate_output=True
)


async def run_login_agent():
    print("--->","Running setup")
    await login_agent.run()

async def run_tear_down():
    print("Running tear down")
    await tear_down.run()
    await browser_context.close()
    await browser.close()

async def run_iot_001():
    print("Running test case iot_001")
    await iot_001.run()

async def run_iot_002():
    print("Running test case iot_002")
    await iot_002.run()

async def test_main(test_case: str = ""):
    await run_login_agent()

    if test_case == "iot_001":
        await run_iot_001()
    elif test_case == "iot_002":
        await run_iot_002()
    else:
        print("No test case specified or unknown ID. Running all test cases...")
        await run_iot_001()
        await run_iot_002()

    await run_tear_down()

if __name__ == "__main__":
    test_case_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    asyncio.run(test_main(test_case_arg))

