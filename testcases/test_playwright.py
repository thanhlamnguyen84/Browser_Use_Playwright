import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import BaseModel, SecretStr, ConfigDict
from playwright.async_api import expect
from dotenv import load_dotenv
from function.test_verify_text import verify_text
from config.credentials import *


task_1 = (
"Open https://web.test.iotportal.com"
f"input username '{USERNAME1}' and password '{PASSWORD1}'"
"Click Setting left menu, then click Time Zone Setting"
)

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
    viewport_expansion=0
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

# Create agent_browser with the model and browser context
agent = Agent(
    task=task_1,
    llm=llm,
    browser_context=browser_context

	# use_vision=True
    # controller=controller
)

agent2 = Agent(
    task=(
        "click About left menu"
        "Click Teams of Service button"
        f"Verify open the '{TERMS_OF_SERVICE_URL}' as a new Tab"
    ),
    llm = llm,
    browser_context = browser_context
)


async def test_main():

    await agent.run()
    page = browser.playwright_browser.contexts[0].pages[0]
    expect(page.get_by_role("button", name="Europe/Zagreb (UTC +02:00)")).to_be_visible()

    await agent2.run()
    # page = browser.playwright_browser.contexts[0].pages[0]
    # await page.pause()
    # expect(page.get_by_role("heading", name="Users")).to_be_visible()
    # expect(page.get_by_role("heading", name="Networks")).to_be_visible()
    # expect(page.get_by_role("heading", name="Devices")).to_be_visible()
    # await agent2.run()

    await browser_context.close()
    await browser.close()


asyncio.run(test_main())
