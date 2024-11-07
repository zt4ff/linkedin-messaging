import time
import os
import random
import platform
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

message_template_path = "./message_template.txt"


def get_message_template():
    with open(message_template_path, "r") as file:
        return file.read()


def login(page):
    page.goto("https://www.linkedin.com/login")
    page.fill("input#username", LINKEDIN_EMAIL)
    page.fill("input#password", LINKEDIN_PASSWORD)
    page.press("input#password", "Enter")
    time.sleep(2)


def send_message(page, profile_url, first_name):
    page.goto(profile_url)
    time.sleep(2)

    try:
        message_button = page.get_by_role("button", name=f"Message {first_name}")
        message_button.click()
    except Exception as e:
        print(f"Could not open message window for {profile_url}. Error: {e}")
        return False

    time.sleep(2)

    message_template = get_message_template()
    message_content = message_template.format(first_name=first_name)

    message_box = page.locator("div[role='textbox']")

    # Irregular typing simulation
    for char in message_content:
        message_box.type(char)
        time.sleep(
            random.uniform(0.05, 0.2)
        )  # Delay between 50ms and 200ms for each character

    if platform.system() == "Darwin":
        message_box.press("Meta+Enter")
    else:
        message_box.press("Control+Enter")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            login(page)
            connections = [
                {
                    "profile_url": "https://www.linkedin.com/in/mike-jay-15b6532b1/",
                    "first_name": "Mike",
                },
            ]

            for connection in connections:
                send_message(page, connection["profile_url"], connection["first_name"])

        finally:
            browser.close()


if __name__ == "__main__":
    main()
