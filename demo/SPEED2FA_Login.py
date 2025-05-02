# main.py

import sys
import os
# Dynamically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr, ConfigDict
from agent_browser.login_agent import run_login_flow
from dotenv import load_dotenv
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from config.credentials import *

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
    browser_window_size={'width': 1024, 'height': 600},
    locale='vi-VN',
    highlight_elements=True,
    viewport_expansion=0

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
    await run_login_flow(browser_context, llm, USERNAME, PASSWORD)

    await browser_context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_main())
