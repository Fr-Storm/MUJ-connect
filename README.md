# Muj Connect - Discord Introduction Bot 📇
## Welcome to Muj Connect — a custom Discord bot that automatically formats beautiful introduction posts for new server members based on their selected roles and inputs!

## ✨ Features
- 📜 Slash Command `/intro` to introduce yourself.

- 🧩 Reads user roles (Age, Gender, Specialization, Year) from onboarding selections.

- 🎨 Posts a clean, styled embed in the `#📇intro channel`.

- 🎭 Changes your nickname to your real name (if bot has permissions).

- 🎯 Assigns hobby roles based on your chosen interests (Gaming, Developer, Rider, etc.).
  
- 🔥 Slash Command `/assign` to assign gender roles manually with permission checks.

- 🛡️ `/assign` command restricted to users with Manage Nicknames permission.

- ⚡ Fully automatic, quick, and easy to use.

## 🚀 How It Works
1. On server join, users select roles (Age, Gender, Specialization, Batch) during onboarding.

2. User uses `/intro` command and fills in:

- Name

- Social usernames (Instagram, Snapchat, etc.)

- Hobbies

3. Bot reads their roles and information, generates a stylish embed, and posts it to `#📇intro`!

4. If hobbies match certain keywords, bot auto-assigns the hobby role.

5. Bot attempts to set user's nickname to their real name.

## 📋 Requirements
Python 3.10+

discord.py library

`.env` file with your Discord bot token (DISCORD_TOKEN)

Hosting server (optional: replit / glitch / render)

## ⚙️ Setup Guide
1. Clone the repository or upload files:
```
git clone https://github.com/your-repo/muj-connect.git
cd muj-connect
```
2. Create and activate a virtual environment (optional but recommended).
   
3. Install dependencies:
```
pip install -r requirements. txt
```
4. Configure environment variables:

- Create a .env file.

- Add your bot token:
```
DISCORD_TOKEN=your-bot-token-here
```

5. Set Channel and Guild IDs:

- Update `Intro_channel_id` in `intro.py` with your intro channel ID.

- Update `guild` ID in `main.py` for fast slash command sync.

6. Modify/Change the roles according to your needs, make sure the same roles exist on the server as well.

7. Run the bot:
```
python main.py
```

## 🛠️ File Structure
```
/cogs
  ├── intro.py     # /intro command (user intro system)
  └── assign.py    # /assign command (gender role assignment)
main.py            # Bot entry point
webserver.py       # (Optional) For hosting
.env               # Secret bot token
README.md          # This file
```

## 🧠 Notes
1. Bot requires the following permissions:

- Manage Nicknames

- Manage Roles (for assigning hobbies)

- Send Messages / Embed Links

2. The bot cannot change the nickname of the server owner or roles higher than itself.

3. `/assign` command:

- Only members with the Manage Nicknames permission can use it.

- If a user already has a gender role, they cannot be assigned another.

- Gives an error if the user tries to use it without permissions.

4. This bot is designed for a specific server. Don't forget to update `Roles in Server/Code`, `guild IDs`, and `channel IDs` properly!

## Made by yours truly, with ❤ 
