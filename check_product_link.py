import asyncio
 
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr
import os
from dotenv import load_dotenv
 
task_1 = """"
- Step 1: Open [IoTPortal](https://web.test.iotportal.com).
- Step 2: Verify there are 5 links: About, Term Of Service (2 links), Privacy Policy (2 links)
- Step 3: Verify there is  the field name "username123"
- Step 3: Click on About link
- Step 4: Verify it opens the new web tab: "https://brtsys.com/iotportal/"
- Step 5: Click on "Term Of Service" link on the left 
- Step 6: Verify it opens the new web tab: "https://brtsys.com/terms-of-service/"
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
 
# Create browser context with the BrowserContextConfig
browser_context = BrowserContext(
    browser=browser,
    config=browser_context_config
)
# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(os.getenv('GOOGLE_API_KEY')))

# Create agent_browser with the model and browser context
agent = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context
)
 
 
async def main():
    await agent.run()
 
    # Close the browser context and browser
    await browser_context.close()
    await browser.close()
 
 
asyncio.run(main())
 

 