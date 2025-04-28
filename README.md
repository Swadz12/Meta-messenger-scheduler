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

# Enter runnable directory to access CLI
cd runnable
scheduler.bat

```


## Troubleshooting

### First Time Running

For the first time use, you may need to login manually and add your Chrome profile path.
This path will look somewhat like this:
```bash
C:\Users\--your name--\AppData\Local\Google\Chrome\User Data\Default
```
1. To add the Chrome profile path, run the CLI and select **Option 1**. Follow the on-screen instructions.
2. Once the path is set, choose **Option 3** to log in to your Messenger account. Make sure to check the **"Remember me"** box so you won't need to log in again.
3. Use **debug mode** only during the initial login process.
4. After setup, you can start sending messages using **Option 2**.
