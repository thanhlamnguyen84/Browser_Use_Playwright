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
from pydantic import BaseModel
from typing import List


task_1 = (
f"Open URL '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
"Click the **second** 'Profile' icon with index 5 at the top-right of the page"
"Click Subscription button"
)

class ExtractResults(BaseModel):
    email_value: int
    dashboard_Data_Request_value: int
    data_Download_Request_value: int


controller = Controller(output_model=ExtractResults)
# Create agent_browser with the model and browser context
agent1 = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context
	)

agent2 = Agent(
    task=(
        "Click on 'Token conversion rate' button"
        "In Token Conversion Rate screen, Get Token Consumed values of Resources"
        "Close the popup window"
      ),
    llm = llm,
    browser_context = browser_context,
    max_failures = 1,
    controller=controller
)

agent3 = Agent(
    task=(
          "Click on 'Manage Subscription' button"
          "Verify 'Monthly Allocated Tokens' value is 1,000,000"

      ),
    llm = llm,
    browser_context = browser_context,
    validate_output=True,
    max_failures = 1
)

async def test_main():
    await agent1.run()
    # final_result = history.final_result()
    # print("✅ Final result:\n", final_result)

    # history1 = await agent2.run()
    # result = history1.final_result()
    # result_dict = json.loads(result)
    # print(f"\nEmail value: {result_dict["email_value"]}")
    # print(f"\nData Request value: {result_dict["dashboard_Data_Request_value"]}")
    # print(f"\nData Download Request value: {result_dict["data_Download_Request_value"]}")
    #
    # assert "Email value: 1000" in f"Email value: {result_dict['email_value']}", \
    #     f"Wrong number: expected '1000', got '{result_dict['email_value']}'"
    # assert "Data Request value: 2000" in f"Data Request value: {result_dict['dashboard_Data_Request_value']}", \
    #     f"Wrong number: expected '2000', got '{result_dict['dashboard_Data_Request_value']}'"
    # assert "Data Download Request value: 1000" in f"Data Download Request value: {result_dict['data_Download_Request_value']}", \
    #     f"Wrong number: expected '1000', got '{result_dict['data_Download_Request_value']}'"

    history3 = await agent3.run()

    if not history3.is_done():
        pytest.fail(f"Incorrect value >> Test failed. Final result: {history3.final_result()}")


    # Close the browser context and browser
    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
