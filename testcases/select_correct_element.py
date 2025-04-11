import asyncio

from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr, ConfigDict
import os
from dotenv import load_dotenv
from function.test_verify_text import verify_text
import json
import warnings
import pytest
import sys
 
task_1 = """
Open https://web.test.iotportal.com, login with username 'thanhlamcayvong@gmail.com' and password 'Duy@1610'
Click the **second** 'Profile' icon with index 5 at the top-right of the page
Click Account Settings > Profile Details
Check whether the 'Multifactor Authentication' button is **enabled**
"""


task_2 = """
Navigate to: https://excalidraw.com/.
Click on the pencil icon (with index 40).
Then draw a triangle in the canvas.
Draw the triangle starting from coordinate (400,400).
You can use the drag and drop action to draw the triangle.
"""

 
# Load the environment variables
load_dotenv()
 
# Create BrowserConfig of Browser Use provided
browser_config = BrowserConfig(
    headless=False,
    disable_security=True
    # chrome_instance_path=r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # chrome_instance_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)
 
# Create browser instance with the BrowserConfig
browser = Browser(config=browser_config)
 

# Create BrowserContextConfig of Browser Use provided
browser_context_config = BrowserContextConfig(
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1600, 'height': 900},
    locale='vi-VN',
    highlight_elements=True,
    viewport_expansion=-1,
    # save_recording_path=os.path.join(project_root, 'exports', 'recordings'),
    # trace_path=os.path.join(project_root, 'exports', 'traces')
)

# class ExtractResults(BaseModel):
#     first_label_field_name: str
#     second_label_field_name: str
#     # login_agreement: str
#
# controller = Controller(output_model=ExtractResults)

# Create browser context with the BrowserContextConfig
browser_context = BrowserContext(
    browser=browser,
    config=browser_context_config
)
# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(os.getenv('GOOGLE_API_KEY')))

# Create agent_browser with the model and browser context
agent1 = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context,
    validate_output= True,
    max_failures=1,
    max_actions_per_step=1
	# use_vision=True
    # controller=controller
)

# agent2 = Agent(
#     task=task_2,
#     llm=llm,
#     browser_context=browser_context,
#     validate_output= True,
#     max_failures=1
#     # controller=controller
# )
# @pytest.mark.smoking
async def test_main():
    history = await agent1.run()
    final_result = history.final_result()
    print("✅ Final result:\n", final_result)
    # try:
    #     verify_text(final_result, "The Multifactor Authentication button is enabled")
    #     print("✅ Button enable.")
    # except AssertionError as e:
    #     print(f"❌ Button enable: {e}")
    if "Multifactor Authentication button is disabled" in final_result:
        pytest.fail("Test failed: MFA button is disabled.")
    else:
        print("✅ Test passed: MFA button is enabled or result is acceptable.")
    # Close the browser context and browser
    await browser_context.close()
    await browser.close()
if __name__ == "__main__":
    asyncio.run(test_main())
 

 