# 🛍️ Daily eBay Deal-to-Telegram Bot

A GitHub Actions bot that finds the best Buy-It-Now deals on eBay matching your criteria and sends them to your Telegram.

## Features

- 🔍 Searches eBay for Buy-It-Now listings matching your criteria
- 💰 Filters by maximum price
- 🚫 Blocks listings with unwanted keywords
- 📱 Sends alerts with deep links to the eBay app
- ⏰ Runs daily at 09:00 America/New_York
- 🔄 Retries on failure with exponential backoff

## Setup

1. **Fork this repository**

2. **Configure your search**
   - Edit `config.toml` to set your:
     - Search term
     - Maximum price
     - Blocked keywords

3. **Set up secrets**
   - Go to your fork's Settings → Secrets and Variables → Actions
   - Add these secrets:
     - `EBAY_APP_ID`: Your eBay API key
     - `TG_BOT_TOKEN`: Your Telegram bot token
     - `CHAT_ID`: Your Telegram chat ID

4. **Enable Actions**
   - Go to Actions tab
   - Enable GitHub Actions for this repository

## Local Development

1. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

## Customization

- **Change schedule**: Edit the cron expression in `.github/workflows/daily.yml`
- **Add filters**: Modify the `filter` parameter in `ebay.py`
- **Customize message**: Edit the message template in `telegram.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this for your own projects! 