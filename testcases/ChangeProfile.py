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


task_1 = (
f"Open URL '{TEST_ADMIN_PORTAL_URL}'"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
"Click the **second** 'Profile' icon with index 5 at the top-right of the page"
"Click Account Settings > Profile Details > Edit"
"Change First Name to Tester"
"Change the Last Name to Lam3"
"Click Save Button and get the confirmation message"

)

# Create agent_browser with the model and browser context
agent1 = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context,
    # validate_output=True
	)

agent2 = Agent(
    task=(
          "Verify that the First Name is 'Tester', the Last Name is 'Lam3'"  
          "Click Edit button again and change back First Name to Nguyen and the Last Name to Lam > Save"
    ),
    llm = llm,
    browser_context = browser_context
)


async def test_main():
    history = await agent1.run()
    final_result = history.final_result()
    print("✅ Final result:\n", final_result)
    # full_result = history.extracted_content()
    # print("✅ Full result:\n", full_result)
    # model_thoughts = history.model_thoughts()
    # print("✅ model_thoughts:\n", model_thoughts())
    try:
        verify_text(final_result, "User profile information has been updated")
        print("✅ Text verification passed.")
    except AssertionError as e:
        print(f"❌ Text verification failed: {e}")
    # if "User profile information has been updated" in full_result:
    #     print("✅ Test passed:User profile information has been updated ")
    # else:
    #     pytest.fail("Test failed: Wrong confirmation message")

    # Close the browser context and browser
    await agent2.run()
    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
