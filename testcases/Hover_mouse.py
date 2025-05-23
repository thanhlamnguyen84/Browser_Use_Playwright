
import asyncio
import os
import sys
import pytest
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use import Agent
from playwright.async_api import expect
from config.credentials import *
from config.config import *
from function.test_verify_text import verify_text
from playwright.async_api import expect
from browser_use.controller.service import Controller


task_1 = (
f"Open URL '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
"Click the **second** 'Profile' icon with index 5 at the top-right of the page"
"Click Subscription button"
)

class ExtractResult(BaseModel):
    email_value: int

class ExtractResults(BaseModel):
	posts: List[ExtractResult]

controller = Controller(output_model=ExtractResults)
# Create agent_browser with the model and browser context
agent1 = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context,
    # validate_output=Tru
	)

agent2 = Agent(
    task=(
        "Click on 'Token conversion rate' button"
        "Get the Email value"
      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True,
    max_failures = 1
    # controller=controller
)

agent3 = Agent(
    task=(
          "Click on 'Manage Subscription' button"
          "Verify 'Monthly Allocated Tokens' value is 2,000,000"

      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True,
    max_failures = 1
)

async def test_main():
    history = await agent1.run()
    # final_result = history.final_result()
    # print("✅ Final result:\n", final_result)

    history1 = await agent2.run()
    print("\nExtracted Content:")
    print(history1.extracted_content())  # Content extracted during execution
    data = history1.extracted_content()
    json_data = json.loads(data)
    value = json_data['email_value']
    print("email_value:", value)
    # print("Second Label Field Name:", second_label)
    # Optional: Assertions to check the values
    assert value == "2000", "First label does not match"
    # assert second_label == "Password", "Second label does not match"
    # page = browser.playwright_browser.contexts[0].pages[0]
    # # await page.pause()
    #
    # await expect(page.get_by_role("dialog")).to_contain_text("10")
    # await expect(page.get_by_role("dialog")).to_contain_text("3000 to 33000*")
    # await expect(page.get_by_role("dialog")).to_contain_text("1000")
    # await expect(page.get_by_text("destination and the SMS rate.")).to_be_visible()

    # result = await agent3.run()
    # assert result.get("success", False), f"Validation failed: {result}"

    # Close the browser context and browser
    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
