import paths
import scheduler

def welcome_message():
    print("""
=================================================
              MESSENGER SCHEDULER 
=================================================
    Send messages on Messenger at a specific time.
    """)

def show_menu():
    print("Choose option")
    print("1. Configure path to your Chrome profile")
    print("2. Run")
    print("3. Run in debug mode (might be necessary when running for the first time)")
    print("4. Quit")

    choice = input("\nYour choice: ")
    return choice

def handle_config():
    if not paths.cookies_path_exists():
        print(f"Current path is {paths.get_cookies_path()}")
        change = input("Do you want to change it? (y/n): ").strip().lower()
        if change != 'y':
            return
    paths.set_cookies_path()

def handle_send_message(headless = False):
    if not paths.cookies_path_exists():
        print("Path to cookies not set. Please set it first.")
        paths.set_cookies_path()
    contact = input("Enter the contact name: ").strip()
    messages = []
    print("\n Enter messages to send (one per line). Press Enter twice to finish:")
    while True:
        msg = input("> ")
        if not msg:
            break
        messages.append(msg)
    print("\n Set time schedule for sending chosen messages (Hour, Minute, Second):")
    hour_input = input("Hour > ")
    minute_input = input("Minute > ")
    second_input = input("Second > ")
    target_time = (int(hour_input), int(minute_input), int(second_input))

    paths.CHAT_NAME = contact

    paths.MESSAGES_LIST = messages

    paths.TARGET_TIME = target_time

    print("You are all set, would you like to run the script now? (y/n): ")
    run = input("Your choice: ").strip().lower()
    if run == 'y':
        scheduler.run_script(headless)

def main():
    welcome_message()

    while True:
        choice = show_menu()

        if choice == '1':
            handle_config()
        elif choice == '2':
            if not paths.cookies_path_exists():
                print("\n-----Path to Chrome profile not set, please set it first-----\n")
                continue
            handle_send_message(headless= True)
        elif choice == '3':
            if not paths.cookies_path_exists():
                print("Path to cookies not set. Please set it first.")
                continue
            handle_send_message(headless= False)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()