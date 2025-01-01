#CRYPTOCURRENCY DATA ANALYSIS AND REPORTING WITH EMAIL NOTIFICATION

# Cryptocurrency Data Analysis and Reporting

This Python project fetches cryptocurrency data from the CoinGecko API, processes it, and sends a daily email report with the top 10 cryptocurrencies to buy and sell based on 24-hour price changes.

## Features
- Fetches real-time cryptocurrency data from CoinGecko API
- Analyzes the data and identifies top 10 cryptocurrencies with the highest and lowest price changes
- Sends a daily email with the report and attaches the full dataset
- Runs daily at a specified time using the `schedule` library

## Requirements
- Python 3.x
- Requests
- Pandas
- Python-dotenv
- Schedule
