# JobScoutBot

Telegram bot for finding job vacancies in Kazakhstan. Supports HeadHunter API and allows saving favorite vacancies.

## Features
- 🔍 Search for jobs by city, salary, employment type, specialty, and experience.
- ⭐ Save vacancies to favorites for quick access later.
- ⚙️ User settings: default city, minimum salary, employment type, experience level, number of vacancies per page, show only vacancies with salary.
- 📊 Filters for more precise search.
- Easy integration with other job APIs in the future.

## Installation
1. Clone the repository:
git clone https://github.com/fl0ret/JobScoutBot.git
cd JobScoutBot

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Create a .env file in the project root with your bot token:
BOT_TOKEN=your_telegram_bot_token
Replace your_telegram_bot_token with your actual Telegram bot token.

Usage
Run the bot:
python main.py

Commands
/start – Start the bot and show the main menu
/find – Start a job search
/help – Show help information
/settings –Open user settings

How it works
User selects “🔍 Найти работу” or uses /find.
Bot asks for city, salary, employment type, specialty, and experience.
Bot fetches vacancies from HeadHunter API.
Results are displayed with title, location, salary, experience, and buttons to open vacancy or add to favorites.
User can view favorites via “⭐ Избранное”.

Adding Favorites
Vacancies can be saved to a JSON-based favorites file. Favorites persist between sessions. Users can manage favorites via the bot interface.

Settings
Users can configure default city, minimum salary, employment type (Full-time, Part-time, Remote), experience level, number of vacancies per page, and filter to show only vacancies with salary.

License
This project is licensed under the MIT License. You may use, modify, and distribute the bot, including for commercial purposes, as long as you credit the original author (Nikita "sadguy", "Floret") or the repository: https://github.com/fl0ret/JobScoutBot.

Requirements
Python 3.10+
aiogram
requests
python-dotenv
