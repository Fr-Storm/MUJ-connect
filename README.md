# Muj Connect - Discord Introduction Bot 📇
## Welcome to Muj Connect — a custom Discord bot that automatically formats beautiful introduction posts for new server members based on their selected roles and inputs!

## ✨ Features
- 📜 Slash Command /intro to introduce yourself.

- 🧩 Reads user roles (Age, Gender, Specialization, Year) from onboarding selections.

- 🎨 Posts a clean, styled embed in the #📇intro channel.

- 🎭 Changes your nickname to your real name (if bot has permissions).

- 🎯 Assigns hobby roles based on your chosen interests (Gaming, Developer, Rider, etc.).

- ⚡ Fully automatic, quick, and easy to use.

## 🚀 How It Works
1. On server join, users select roles (Age, Gender, Specialization, Batch) during onboarding.

2. User uses /intro command and fills in:

- Name

- Social links (Instagram, Snapchat, etc.)

- Hobbies

3. Bot reads their roles and information, generates a stylish embed, and posts it to #📇intro!

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
2. Creating a .venv is highly recommended.
   
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
  └── intro.py     # Cog for intro slash command
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

2. Bot cannot change nickname of the server owner or roles higher than itself (Discord restriction).

3. This bot works inside a specific guild for faster command syncing. So, don't forget to change `guild` Id and `Intro_channel_Id` in the code.

## Made by yours truly, with ❤ 
