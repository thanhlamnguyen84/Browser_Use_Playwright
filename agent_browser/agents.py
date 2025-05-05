# agents.py

from browser_use import Agent
from config.credentials import USERNAME1, PASSWORD1
from config.config import TEST_ADMIN_PORTAL_URL, llm
from agent_browser.agents import *

def get_agents(browser_context):
    login_agent = Agent(
        task=(
            f"Open Web '{TEST_ADMIN_PORTAL_URL}'"
            f"input username '{USERNAME1}' and password '{PASSWORD1}' to login"
        ),
        llm=llm,
        browser_context=browser_context
    )

    iot_001 = Agent(
        task=(
            "click 'Add Chart' button"
            "Select Energy Consumption and click Next"
            "Click Select Sensors > input 'Active power - Phase A' in search box"
            "Select checkbox in search result list > click Add button"
            "In chart name column, input 'iot_001chart'"
            "Click create button"
            "Verify the text '1/1 chart(s) are successfully created...' is displays"
            "Click OK and stay there in 10 seconds"
            "Verify that the chart with name 'iot_001chart' displayed in Dashboard"
        ),
        llm=llm,
        browser_context=browser_context,
        validate_output=True
    )

    iot_002 = Agent(
        task=(
            "click 'Add Chart' button"
            "Select Water Consumption and click Next"
            "Click Select Sensors"
            "Select a checkbox > click Add button"
            "In chart name column, input 'iot_002chart'"
            "Click create button"
            "Click OK and stay there in 10 seconds"
            "Verify that the chart with name 'iot_002chart' displayed in Dashboard"
        ),
        llm=llm,
        browser_context=browser_context,
        validate_output=True
    )

    tear_down = Agent(
        task=(
            "Find all the chart with name 'iot001chart' and 'iot002chart' delete them"
        ),
        llm=llm,
        browser_context=browser_context
    )

    return login_agent, iot_001, iot_002, tear_down
