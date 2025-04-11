import asyncio

from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr, ConfigDict
import os
from dotenv import load_dotenv
import json
import warnings
import pytest
import sys
 
task_1 = """"
- Step 1: Open [IoTPortal](https://web.test.iotportal.com).
- Step 2: Get the label of field name and Password

"""
 
# Load the environment variables
load_dotenv()
 
# Create BrowserConfig of Browser Use provided
browser_config = BrowserConfig(
    headless=False,
    disable_security=True,
    # chrome_instance_path=r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # chrome_instance_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)
 
# Create browser instance with the BrowserConfig
browser = Browser(config=browser_config)
 
# Ensure project_root is a string
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
recording_path = os.path.join(project_root, 'exports', 'recordings')
trace_path = os.path.join(project_root, 'exports', 'traces')
 
# Create the directory if it does not exist
if not os.path.exists(recording_path):
    os.makedirs(recording_path)
if not os.path.exists(trace_path):
    os.makedirs(trace_path)
 
# Create BrowserContextConfig of Browser Use provided
browser_context_config = BrowserContextConfig(
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1600, 'height': 900},
    locale='vi-VN',
    highlight_elements=True,
    viewport_expansion=-1,
    save_recording_path=os.path.join(project_root, 'exports', 'recordings'),
    trace_path=os.path.join(project_root, 'exports', 'traces')
)

class ExtractResults(BaseModel):
    first_label_field_name: str
    second_label_field_name: str
    # login_agreement: str

controller = Controller(output_model=ExtractResults)

# Create browser context with the BrowserContextConfig
browser_context = BrowserContext(
    browser=browser,
    config=browser_context_config
)
# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(os.getenv('GOOGLE_API_KEY')))

# Create agent with the model and browser context
agent = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context,
    controller=controller,
    validate_output=True
)
 
# @pytest.mark.smoke
async def test_main():
    history = await agent.run()
    print("\nExtracted Content:")
    print(history.extracted_content())  # Content extracted during execution
    data = history.extracted_content()
    if not data:
        print("No extracted content found.")
        return

    # Convert JSON to readable text
    def json_to_text(obj, indent=0):
        if isinstance(obj, dict):
            return "\n".join(f"{' ' * indent}{k}: {json_to_text(v, indent + 2)}" for k, v in obj.items())
        elif isinstance(obj, list):
            return "\n".join(f"{' ' * indent}- {json_to_text(v, indent + 2)}" for v in obj)
        else:
            return str(obj)

    text1 = json_to_text(data)
    print("\n🔹 Extracted Content:\n", text1)
    assert "Email / Mobile Number" == text1["first_label_field_name"]
    assert "Password" == text1["second_label_field_name"]

        # print(f"\nKết qua got: {text["second_label_field_name"]}")
    # print(f"\nKết qua got: {result_dict["login_agreement"]}")

    # assert "Password" == "Password" in text["second_label_field_name"]
    # assert "By logging into an account, you are agreeing with our Terms of Service and Privacy Policy and you confirm that you are above 13 years of age." in result_dict["login_agreement"]

    # Close the browser context and browser
    await browser_context.close()
    await browser.close()

asyncio.run(test_main())
 

 