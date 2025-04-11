# main.py

import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr, ConfigDict
from agent_browser.login_agent import run_login_flow
import os
from dotenv import load_dotenv
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from config.credentials import USERNAME, PASSWORD

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



# Create browser context with the BrowserContextConfig
browser_context = BrowserContext(
    browser=browser,
    config=browser_context_config
)
# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(os.getenv('GOOGLE_API_KEY')))

async def test_main():

    user = USERNAME
    password = PASSWORD
    await run_login_flow(browser_context, llm, user, password)

    await browser_context.close()
    await browser.close()
if __name__ == "__main__":
    asyncio.run(test_main())
