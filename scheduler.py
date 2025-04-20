import time
import os
import paths
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pytz
from datetime import datetime, timedelta

USER_DATA_DIR = paths.USER_DATA_DIR
CHAT_NAME = paths.CHAT_NAME
#to fill
MessagesList = paths.MESSAGES_LIST
TARGET_TIME = paths.TARGET_TIME

def find_and_click_contact(page, contact_name =CHAT_NAME):

    print(f"Finding contact {contact_name}...")
    search_bar = 'input[role="combobox"]'

    page.wait_for_selector(search_bar)
    page.click(search_bar)

    print(f'typing contact name: {contact_name} in ')
    page.keyboard.type(contact_name)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)

    chat_selector = f'text="{contact_name}" >>nth = 1'
    page.wait_for_selector(chat_selector)
    page.click(chat_selector)
    print(f"Chat chosen {CHAT_NAME}.")
    page.wait_for_timeout(3000)



def waitForCorrectTime():
    polish_tz = pytz.timezone("Europe/Warsaw")

    now = datetime.now(polish_tz)

    print("Current time is:", now)
    target_time = now.replace(hour=TARGET_TIME[0],minute=TARGET_TIME[1],second=TARGET_TIME[2],microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    print(f"Waiting for {wait_seconds} seconds until {target_time}...")
    time.sleep(wait_seconds)

    print(f"Current time is {datetime.now(polish_tz)}. Proceeding to send message.")
    send_message()

def send_message():
    print(f"Attempting to un chrome with profile: {USER_DATA_DIR}")

    with sync_playwright() as p:
        context = None
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                channel="chrome",
                args=[
                    '--start-maximized',
                    '--disable-blink-features=AutomationControlled'
                ],
            )
            print("Chromium context opened.")

            page = context.new_page()
            page.set_extra_http_headers({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            })
            print("Navigating to messenger")

            page.goto("https://messenger.com", wait_until="domcontentloaded", timeout=1000000)
            chat_selector = f'text="{CHAT_NAME}"'
            return find_and_click_contact(page)
            page.wait_for_selector(chat_selector)
            page.click(chat_selector)
            print(f"Chat chosen {CHAT_NAME}.")
            print(f"Loaded, title: {page.title()}")

            page.wait_for_selector(r'div[contenteditable="true"][role="textbox"]')
            page.click(r'div[contenteditable="true"][role="textbox"]')


            #Send messages separately if needed
            for i in range(len(MessagesList)):
                MESSAGE_TEXT = MessagesList[i]
                print(f"sending msg: {MESSAGE_TEXT}")
                page.keyboard.type(MESSAGE_TEXT)
                page.keyboard.press("Enter")
            sent_message_selector = f'div[role="row"]:has-text("{MESSAGE_TEXT}")'
            page.wait_for_selector(sent_message_selector, state="visible")
            print(f"message '{MessagesList}' sent to {CHAT_NAME}.")
            last_message = paths.MESSAGES_LIST[-1]
            page.wait_for_function(
                f'document.body.textContent.includes("{last_message}")'
            )
            page.wait_for_timeout(5000)

        except PlaywrightTimeoutError as pe:
            print(f"Timeout : {pe}")
        except Exception as e:
            print(f"unexpected err: {e}")
        finally:
            # input("enter to close:")
            context.close()
            print("Script finished")

if __name__ == "__main__":
    send_message()