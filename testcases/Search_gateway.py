
import asyncio
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use import Agent
from playwright.async_api import expect
from config.credentials import *
from config.config import *
from function.test_verify_text import verify_text
from playwright.async_api import expect


task_1 = (
f"Open URL '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
"Click the Gateways left menu"
)

# Create agent_browser with the model and browser context
agent1 = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context
    # validate_output=True
	)

agent2 = Agent(
    task=(
        "Click sort icon for UUID column"
        "Verify that the UUIDs are sorted in descending order"
        "Click sort icon for UUID column again"
        "Verify that the UUIDs are sorted in ascending order (smallest → largest)"
      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True,
    max_failures = 1,
)

agent3 = Agent(
    task=(
          "Get all Gateways name"

      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)

async def test_main():
    history = await agent1.run()
    final_result = history.final_result()
    print("✅ Final result:\n", final_result)

    await agent2.run()
    final_result = history.final_result()
    print("✅ Final result:\n", final_result)

    await agent3.run()
    print("✅ Final result:\n", final_result)


    # Close the browser context and browser
    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
