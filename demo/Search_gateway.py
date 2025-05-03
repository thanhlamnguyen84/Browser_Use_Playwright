
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
import re
import json


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
        "Click sort icon 1 time for UUID column"
        "Verify that the UUIDs are sorted in **descending** order (largest -> smallest) "

      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True,
    max_actions_per_step=3,
    max_failures = 1,
)

agent3 = Agent(
    task=(
          "Input PCS in the search box"
          "Verify that the search result just has the gateway names which contain PCS text"

      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True
)

async def test_main():
    print("\n...Setting up for the test")
    await agent1.run()
    print("Running the sort test")
    history2 = await agent2.run()
    result = history2.action_results()
    print("✅ Action result:\n", result)
    action_result = json.loads('{"success": false}')
    assert action_result not in result, "❌ Test failed: wrong sort order"
    print("✅ Test sort descending passed")
    new_task = (
        "Click sort icon 1 time for UUID column"
        "Verify that the UUIDs are not sorted in **ascending** order (smallest → largest)"
    )
    agent2.add_new_task(new_task)
    history3 = await agent2.run()
    result_new = history3.action_results()
    print("✅ Action result:\n", result_new)
    action_result2 = json.loads('{"success": false}')
    assert action_result2 not in result_new, "❌ Test failed: wrong sort order"
    print("✅ Test sort ascending passed")

    print("Running the sort test")
    history4=await agent3.run()
    result4 = history4.final_result()
    print("✅ Final result 4:\n", result4)

    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
