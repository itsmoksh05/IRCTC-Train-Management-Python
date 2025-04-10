# IRCTC Python Train Management System 🚆🐍

A command-line Python application that interfaces with the IRCTC API to provide real-time information about Indian Railways. It helps users with:

- 📍 Station-wise train lookup  
- 🧾 PNR status tracking  
- 🗓️ Train schedules  
- 🧭 Trains between stations  
- 💺 Seat availability  
- 💰 Fare checks

## 🚀 Features

- Interactive CLI with a user-friendly menu
- Uses real-time API data for accuracy
- Tabular data display using `tabulate`
- `.env` support for API credentials
- Modular, clean code structure

## 🛠️ Tech Stack

- Python 3
- `requests` for API calls
- `tabulate` for clean terminal tables
- `dotenv` for secure API keys

## 📦 Installation

```bash
git clone https://github.com/itsmoksh05/IRCTC-Train-Management-Python.git
cd IRCTC-Train-Management-Python
pip install -r requirements.txt
```
## 🔑 API Key Setup

To configure the environment and use the Indian Railways API:

1. Create a `.env` file in the root directory of the project.
2. Add the following lines:

```env
ENV_API_KEY=<your_actual_api_key>
BASE_URL=https://indianrailapi.com/api/v2/
```
3. Replace <your_actual_api_key> with the API key you received from [Indian Railways API Collection](https://indianrailapi.com/api-collection).

⚠️ Keep your .env file safe and do NOT share it publicly or commit it to GitHub.

## Usage
Run the script using Python:
```bash
python IRCTC.py
```

> 🛠️ [A Moksh Production](https://github.com/codewithmoksh) – from chaos to clarity, transforming logic into legacy.
