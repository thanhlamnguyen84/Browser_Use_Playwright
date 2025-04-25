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


task_1 = (
f"Open '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
)

# Create agent_browser with the model and browser context
agent = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context
	)

agent1 = Agent(
    task=(
        "click About left menu"
        f"Verify software version is '{IOT_WMC_VERSION}'"
        "Click 'Terms of Service'"
              f"Verify page '{TERMS_OF_SERVICE_URL}' is opened."
        f"Close the second Tab with URL '{TERMS_OF_SERVICE_URL}'"
        ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)
agent2 = Agent(
    task=(
       "Click Privacy Policy button"
            f"Verify page '{PRIVACY_POLICY_URL}' is opened"
    ),
    llm = llm,
    browser_context = browser_context
)

agent3 = Agent(
    task=(
        "click About left menu"
        "Click Licenses button"
            f"Verify page '{LICENSE_URL}' is opened"
    ),
    llm = llm,
    browser_context = browser_context
)
async def test_main():
    #Login
    await agent.run()
    #Verify version number
    await agent1.run()
    # await agent2.run()
    # await agent3.run()

    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
