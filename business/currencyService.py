import os
from requests import get
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

class CurrencyService:
    api_key = os.getenv("APY_KEY")

    def get_key_list(self):
        url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={self.api_key}"
        req = get(url)
    
        req_json = req.json()
        
        rates = req_json['rates']

        return list(rates.keys())

    def get_rate(self,COD):
        specific_url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={self.api_key}&symbols={COD},ARS"
        req = get(specific_url)

        req_json = req.json()

        rates_str = req_json['rates']

        rate_ARS_str = rates_str['ARS']
        rate_COD_str = rates_str[COD]

        rate_ARS_decimal = Decimal(rate_ARS_str)
        rate_COD_decimal = Decimal(rate_COD_str)
        
        rate_COD_ARS = rate_ARS_decimal / rate_COD_decimal

        return rate_COD_ARS