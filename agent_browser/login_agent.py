# agent_browser/login_agent.py

from function.get_2FA_code_Outlook import get_2fa_code_from_outlook
from playwright.async_api import async_playwright
import asyncio
from config.credentials import USERNAME
async def run_login_flow(browser_context, llm, user, password):
    from browser_use.agent.service import Agent
    # Fetch 2FA code from Outlook

    agent1 = Agent(
        task=(
            "go to https://web.test.iotportal.com, hit Forgot Password"
            f"input username '{USERNAME}' and click Reset Password"
            "wait for Forgot Password page displays"

        ),
        llm=llm,
        browser_context=browser_context
    )

    await agent1.run(max_steps=10)

    otp_code = get_2fa_code_from_outlook(user=user, password=password, mail_server_url='outlook.office365.com')
    print(f"OTP Code= {otp_code}")

    agent2 = Agent(
        task=(
            f"input 6 digits of real OTP code: {otp_code} to verification code input field"
            "Click Submit button"
        ),
        llm=llm,
        browser_context=browser_context
    )

    await agent2.run(max_steps=10)