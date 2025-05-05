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
"Open https://web.test.iotportal.com"
f"input username '{USERNAME1}' and password '{PASSWORD1}' to login"
)

# Create agent_browser with the model and browser context
login_agent = Agent(
    task=login,
    llm=llm,
    browser_context=browser_context

	)

iot_1234 = Agent(
    task=(
        "click 'Add Chart' button"
        "Select Energy Consumption and click Next"
        "Click Select Sensors > input 'Active power - Phase A' in search box"
        "Select checkbox in search result list > click Add button"
        "In chart name column, input 'iot1234chart'"
        "Click create button"
        "Verify the text '1/1 chart(s) are successfully created...' is displays"
        "Click OK and stay there in 10 seconds"
        "Verify that the chart with name 'iot1234chart' displayed in Dashboard"
    ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)

tear_down = Agent(
    task=(
        "Find the chart with name 'iot1234chart' and delete it"
    ),
    llm = llm,
    browser_context = browser_context
    # validate_output=True
)

async def test_main():
    print ("Running setup")
    await login_agent.run()
    print("Running test case iot_1234")
    await iot_1234.run()

    # await page.pause()
    print("Running tear down")
    await tear_down.run()
    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())