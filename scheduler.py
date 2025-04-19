import time
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

USER_DATA_DIR = r"C:\Users\swadz\AppData\Local\Google\Chrome\User Data\Default"
WAIT_TIME_SECS = 20
CHAT_NAME = "Name"
MessagesList = ["Msg1", "Msg2", "Msg3", "Msg4", "Msg5"]
def send_message():
    print(f"Attemptowanie uruchomienia Chrome z profilem: {USER_DATA_DIR}")
    print("Upewnij się, że Chrome korzystający z tego profilu jest zamknięty.")

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
                timeout = 110000
            )
            print("Kontekst przeglądarki uruchomiony.")

            page = context.new_page()
            page.set_extra_http_headers({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            })
            print("Nawigowanie do messenger.com...")

            page.goto("https://messenger.com", wait_until="domcontentloaded", timeout=1000000)
            chat_selector = f'text="{CHAT_NAME}"'
            page.wait_for_selector(chat_selector)
            page.click(chat_selector)
            print(f"Chat chosen {CHAT_NAME}.")
            print(f"Strona załadowana. Tytuł: {page.title()}")

            page.wait_for_timeout(3000)

            page.wait_for_selector(r'div[contenteditable="true"][role="textbox"]')
            page.click(r'div[contenteditable="true"][role="textbox"]')
            for i in range(len(MessagesList)):
                MESSAGE_TEXT = MessagesList[i]
                print(f"Wysyłanie wiadomości: {MESSAGE_TEXT}")
                page.keyboard.type(MESSAGE_TEXT)
                page.keyboard.press("Enter")
            page.wait_for_timeout(3000)

            print(f"Wiadomość '{MESSAGE_TEXT}' wysłana do {CHAT_NAME}.")

            page.wait_for_timeout(3000)


        except PlaywrightTimeoutError as pe:
            print(f"Playwright Timeout Error podczas uruchamiania lub nawigacji: {pe}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
        finally:
            # Zamiast automatycznego zamykania, czekamy na akcję użytkownika.
            input("Naciśnij Enter, aby zamknąć przeglądarkę...")
            context.close()
            print("Skrypt zakończony.")

if __name__ == "__main__":
    send_message()