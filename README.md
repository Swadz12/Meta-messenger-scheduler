# Messenger Scheduler

A Python tool that automatically schedules and sends messages at specified times. Script does it directly through Messenger.com utilizing *Playwright* library.

## Features

- ✅ Schedule as many messages as you like
- ✅ It supports sending messages separately so it looks natural for receiver.
- ✅ It utilizes exisiting Chrome cookies, so its not necessary to login each time it runs.
- ✅ It's configurable through cmd, though it can be managed via python code.

## Requirements

- Python 3.8+
- Playwright
- Google Chrome browser
- pytz

## Installation

```bash
# Clone the repository
git clone https://github.com/Swadz12/Meta-messenger-scheduler.git
cd Meta-messenger-scheduler

# Install dependencies
pip install -r reqs.txt

# Install Playwright browsers
playwright install chromium
```

## Config

Edit `paths.py` to change default settings:

```python
USER_DATA_DIR = r'C:\Users\username\AppData\Local\Google\Chrome\User Data\Default'
CHAT_NAME = 'Contact Name'
MESSAGES_LIST = ['Example message']
TARGET_TIME = [17, 25, 0]  # hour, minute, second
```

## Usage

### Basic Execution

```bash
python main.py --help 
```

### Example usage, after reading - -help note

```bash
python main.py 
--contact "John Doe" 
--messages "Message 1" "Message 2" 
--time 18 30 0 
--run
```
**I suggest to set Cookies path directly in your Python IDE before running**

### Command Line Arguments

- `--profile` - path to Chrome user profile (Cookies, suggested to hardcode)
- `--contact` - contact name to search for
- `--messages` - list of messages to send
- `--time` - sending time [hour minute second]
- `--run` - execute script immediately

## Troubleshooting

### First Time Login

For first-time use, you may need to login manually:
1. Navigate to **paths.py** and manually change USER_DATA_DIR
2. Navigate to ***scheduler.py***
3. Change `headless=True` to `headless=False` in the `send_message()` function
4. Uncomment the line `# page.wait_for_timeout(100000000)`
5. Run the script and login manually
6. Make sure to check the "Stay logged in" option

### Issues with Special Characters

If you experience issues with contacts having special characters in their names, uncomment the code related to Polish characters in the `find_and_click_contact()` function.
