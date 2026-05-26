# PIHPS Commodity Alert Bot

A Telegram bot that monitors Indonesian food commodity prices (PIHPS) and sends automated alerts when significant price changes occur.

---

## Features

- Automated daily data fetching from PIHPS API
- Price change detection per commodity
- Configurable percentage threshold alerts
- Province-based monitoring
- Telegram bot interface
- Duplicate alert prevention
- National summary analytics command
- Scheduled background job execution

---

## System Architecture

1. Fetch data from PIHPS API
2. Normalize and store in SQLite database
3. Analyze price changes
4. Filter based on threshold
5. Check duplicate alerts
6. Send Telegram notifications

---

## Key Commands

### Bot Commands
- `/start` → Start bot
- `/setprovince <province>` → Set your province
- `/mysettings` → View your settings
- `/national [threshold]` → View nationwide price changes

---

## Tech Stack

- Python
- SQLite

---

## Database

Uses SQLite:
- stores price history
- stores user preferences
- stores sent alerts (deduplication)
