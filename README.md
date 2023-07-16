## What is TelegramSpammer?

This bot will allow you to extract users from other groups, add users to your groups, clone groups, send mass private messages, and many more options.

## Install dependencies

```bash
pip install -r requeriments.txt
```

## Configuration

Introduce the configuration of your users in the clients.py file located inside the data folder.

This file has the following format:

```json
    "clients": [
        {
            "user" : "user_name1",
            "api_id" : 666666,
            "api_hash" : "a90s8435rcrw65d6c1a479dd7d9731de",
            "phone":"+34666666666",
            "device_model": "[STRING]",
            "system_version":  "[STRING]",
            "app_version": "[STRING]",
            "system_lang_code": "[STRING]",
            "lang_pack": "[STRING]",
            "lang_code": "[STRING]"
        },
        {
            "user" : "user_name2",
            "api_id" : 777777,
            "api_hash" : "a90s8435rcrw65d6c1a479dd7d9731de",
            "phone":"+34666666667",
            "device_model": "[STRING]",
            "system_version":  "[STRING]",
            "app_version": "[STRING]",
            "system_lang_code": "[STRING]",
            "lang_pack": "[STRING]",
            "lang_code": "[STRING]"
        }
    ]
```

## Avoid being banned!
Due to the large number of users who have used the Telethon library for spamming, Telegram has implemented certain security measures.

To prevent your account from being deactivated, blocked, or banned:

Log in Telegram official client on your desktop, enable debug mode, collect some logs (write a message), and check the following parameters:

    api_id: [INT],
    device_model: [STRING],
    system_version:  [STRING],
    app_version: [STRING],
    system_lang_code: [STRING],
    lang_pack: [STRING],
    lang_code: [STRING],

To enable debug mode just type 'debugmode' in the settings page of Telegram desktop and confirm it.
Logs will be saved C:\Users\USER_NAME\AppData\Roaming\Telegram Desktop

Make sure you have the same settings when instantiating TelegramClient class.

## RUN

```bash
python main.py
```
