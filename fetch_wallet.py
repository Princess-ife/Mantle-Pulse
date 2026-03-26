import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

#WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
BASE_URL = "https://api.etherscan.io/v2/api"

def fetch_wallet_transactions(WALLET_ADDRESS):
    params = {
       "chainid": "5000",
       "module": "account",
       "action": "txlist",
       "address": WALLET_ADDRESS,
       "sort": "desc",
       "apikey": os.getenv("API_KEY")
   }


    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data["status"] == "1":
        df = pd.DataFrame(data["result"])
        print(f"Found {len(df)} transactions")
        print(df[["hash", "from", "to", "value", "timeStamp"]].head())
        return df
    else:
      error_msg = data.get('message', 'Invalid Mantle wallet or API connection failed')
      raise Exception(f"Error: {error_msg}")

#fetch_wallet_transactions(WALLET_ADDRESS)
