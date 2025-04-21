# paths.py
import argparse

#Path to directory where Cookies are stored
USER_DATA_DIR = r'C:\Users\swadz\AppData\Local\Google\Chrome\User Data\Default'
CHAT_NAME = 'Jan Kowalski' #be careful with names
MESSAGES_LIST = [] #for testing purposes might be empty
TARGET_TIME = [17, 25, 0]

def parse_cli_args():
    parser = argparse.ArgumentParser(description="Messenger Scheduler")
    parser.add_argument('--profile', help='Path to Chrome profile', default=USER_DATA_DIR)
    parser.add_argument('--contact', help='Name of contact', default=CHAT_NAME)
    parser.add_argument('--messages', nargs='*', help='List of messages to send', default=MESSAGES_LIST)
    parser.add_argument('--time', nargs=3, type=int, help='Time to send message (hour minute second)', default=TARGET_TIME)
    parser.add_argument('--run', action='store_true', help='Run script immediately')
    args = parser.parse_args()
    return args

def update_config_from_args(args):
    global USER_DATA_DIR, CHAT_NAME, MESSAGES_LIST, TARGET_TIME
    USER_DATA_DIR = args.profile
    CHAT_NAME = args.contact
    MESSAGES_LIST = args.messages
    TARGET_TIME = args.time
    print("Configuration updated.")