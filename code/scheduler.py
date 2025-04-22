import time
import paths
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pytz
from datetime import datetime, timedelta

class Config:
    def __init__(self, user_data_dir, chat_name, messages_list, target_time):
        self.user_data_dir = user_data_dir
        self.chat_name = chat_name
        self.messages_list = messages_list
        self.target_time = target_time

config = Config("","", [], [])

def run_script(debug_mode):
    global config
    if not paths.cookies_path_exists():
        paths.set_cookies_path()
    paths.USER_DATA_DIR = paths.get_cookies_path()

    config = Config(paths.USER_DATA_DIR, paths.CHAT_NAME, paths.MESSAGES_LIST, paths.TARGET_TIME)
    waitForCorrectTime(debug_mode)

def find_and_click_contact(page):

    page.wait_for_timeout(1000)
    contact_name = config.chat_name
    print(f"Finding contact {contact_name}...")
    search_bar = 'input[role="combobox"]'
    page.wait_for_timeout(1000)

    page.wait_for_selector(search_bar)
    page.click(search_bar)

    print(f'typing contact name: {contact_name} in ')
    page.keyboard.type(contact_name)
    page.keyboard.press("Enter")
    page.wait_for_selector(search_bar)
    page.wait_for_timeout(2000)

    #Quick solve with polish characters
    # polish_chars = set('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ')
    # has_polish_chars = any(char in contact_name for char in polish_chars)
    # if has_polish_chars:
    #     nth_index = 1
    # else:
    nth_index = 1
    chat_selector = f'text="{contact_name}">>nth={nth_index}'
    page.wait_for_selector(chat_selector)
    page.wait_for_timeout(2000)
    page.click(chat_selector)
    print(f"Chat chosen {contact_name}.")
def waitForCorrectTime(headless):
    polish_tz = pytz.timezone("Europe/Warsaw")

    now = datetime.now(polish_tz)

    print("Current time is:", now)
    target_time = now.replace(
        hour=config.target_time[0],
        minute=config.target_time[1],
        second=config.target_time[2],
        microsecond=0
    )
    if now > target_time:
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    print(f"Waiting for {wait_seconds} seconds until {target_time}...")
    time.sleep(wait_seconds)

    print(f"Current time is {datetime.now(polish_tz)}. Proceeding to send message.")
    send_message(headless)

def send_message(headless):
    print(f"Attempting to un chrome with profile: {config.user_data_dir}")

    with sync_playwright() as p:
        context = None # Initialize context to None so it can be always closed in finally block
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=config.user_data_dir,
                headless=headless, # Set to True if you want to run in headless mode
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
            #Somtimes it might be necessary to log in (only once, then cookies are saved),
            #if situtation like this occur, run following line:
            if not headless:
                page.wait_for_timeout(100000000) #time to log in manually
            find_and_click_contact(page)

            page.wait_for_selector(r'div[contenteditable="true"][role="textbox"]')
            page.click(r'div[contenteditable="true"][role="textbox"]')
            page.wait_for_timeout(2000)
            #Send messages separately if needed

            for i in range(len(config.messages_list)):
                MESSAGE_TEXT = config.messages_list[i]
                print(f"sending msg: {MESSAGE_TEXT}")
                page.keyboard.type(MESSAGE_TEXT)
                page.keyboard.press("Enter")
            sent_message_selector = f'div[role="row"]:has-text("{MESSAGE_TEXT}")'
            page.wait_for_selector(sent_message_selector, state="visible")

            print(f"message '{config.messages_list}' sent to {config.chat_name}.")
            last_message = config.messages_list[-1]
            page.wait_for_function(
                f'document.body.textContent.includes("{last_message}")'
            )
            page.wait_for_timeout(2000)

        except PlaywrightTimeoutError as pe:
            print(f"Timeout : {pe}")
        except Exception as e:
            print(f"unexpected err: {e}")
        finally:
            # input("enter to close:")
            context.close()
            print("Script finished")