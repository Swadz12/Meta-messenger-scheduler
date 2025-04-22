# paths.py
import argparse
import json
import os

#Path to directory where Cookies are stored
USER_DATA_DIR = ""
CHAT_NAME = "" #be careful with names
MESSAGES_LIST = [] #for testing purposes might be empty
TARGET_TIME = [0, 0, 0]

CONFIG_FILE = 'cookies_path.json'

def cookies_path_exists():
    global CONFIG_FILE
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            if os.path.exists(data["USER_DATA_DIR"]):
                return True
            else:
                return False
    else:
        return False

def get_cookies_path():
    global CONFIG_FILE
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data["USER_DATA_DIR"]
    else:
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please set the cookies path.")

def is_cookies_path(path):
    to_match = "Default"
    if path[-len(to_match):] == to_match:
        return True
    return False
def set_cookies_path():
    while True:
        path = input("Enter the path to your Chrome profile: ").strip()
        if os.path.exists(path):
            if not is_cookies_path(path):
                print("\nYour path is syntax valid, but does not point to the correct directory.\n"
                      "Path will be structured like this: C:\\Users\\-your name-\\AppData\\Local\\Google\\Chrome\\User Data\\Default \n" )
                continue
            save_cookies_path(path)
            break
        else:
            print("Invalid path")

def save_cookies_path(path):
    config = {"USER_DATA_DIR": path}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

    if cookies_path_exists():
        print("\n")
        print("Congratulations, you have successfully set the path to your cookies, from now you won't be asked for it again.")
        print("\n")




def parse_cli_args():
    parser = argparse.ArgumentParser(description="Messenger Scheduler")
    parser.add_argument('--contact', help='Name of contact', default=CHAT_NAME)
    parser.add_argument('--messages', nargs='*', help='List of messages to send', default=MESSAGES_LIST)
    parser.add_argument('--time', nargs=3, type=int, help='Time to send message (hour minute second)', default=TARGET_TIME)
    parser.add_argument('--run', action='store_true', help='Run script immediately')
    args = parser.parse_args()
    return args

def update_config_from_args(args):
    global USER_DATA_DIR, CHAT_NAME, MESSAGES_LIST, TARGET_TIME
    CHAT_NAME = args.contact
    MESSAGES_LIST = args.messages
    TARGET_TIME = args.time
    print("Configuration updated.")