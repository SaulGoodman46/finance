import yfinance as yf
import subprocess
import platform
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

class portfolio_manager:

    def __init__(self):
        pass

    def ping(self, host):
        """
        Ping a host to check for internet connectivity.
        
        Args:
        host (str): The host to ping (e.g., 'google.com').
        
        Returns:
        bool: True if the host is reachable, False otherwise.
        """
        # Determine the command based on the operating system
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        
        # Build the command
        command = ['ping', param, '1', host]
        
        # Execute the command
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check the return code
        return response.returncode == 0

    def read_csv(self):
        file_name = "INPUTS/transactions.csv"
        
        print("Reading transactions.csv...\nPlease Wait")

        df = pd.read_csv(file_name)

        transaction_dict = {}
        first = 0
        tmp_dict = {}
        for row in df.values:
            ticker                  = row[2].strip()
            print(f"Ticker: {ticker} found\n in row {row}")
            tmp_dict["type"]        = row[0]
            tmp_dict["stock_name"]  = row[1]
            tmp_dict["date"]        = row[3]
            tmp_dict["quantity"]    = row[4]
            tmp_dict["value"]       = row[5]
            transaction_dict[ticker] = tmp_dict

            print(f"Loaded ticker {ticker} with values {transaction_dict[ticker]}")

        return transaction_dict
    
    def get_stock_price_by_ticker(self, ticker):
        if not ticker:
            raise ValueError(f"Ticker not found: {ticker}")

        # Recupera i dati dell'azione utilizzando il ticker
        stock = yf.Ticker(ticker)

        # Ottieni il prezzo attuale
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        print(f"Il prezzo attuale di {ticker} è: {current_price}")

        if current_price is None:
            raise ValueError(f"Prezzo non disponibile per il ticker: {ticker}")

        return current_price

    def get_current_values(self, stock_dict):
        for key in stock_dict.keys():
            tmp_dict = stock_dict[key]

            print(f"Downloading ticker {key} value")
            print(f"Ticker: {key} found value {self.get_stock_price_by_ticker(key)}")
            
            tmp_dict["cprice"] = self.get_stock_price_by_ticker(key)
            tmp_dict["cvalue"] = tmp_dict["cprice"] * tmp_dict["quantity"]
            tmp_dict["profit"] = tmp_dict["cvalue"] - (tmp_dict["value"] * tmp_dict["quantity"])
            print(f"Profit for {tmp_dict['stock_name']} is {tmp_dict['profit']}")

            stock_dict[key] = tmp_dict


    def plot_portfolio_chart(self, stock_dict):
        
        # compute total value
        total_value = 0
        for key, value in stock_dict.items():
            total_value += value["cprice"] * value["quantity"]

        # Compute relative weight
        for key, value in stock_dict.items():
            stock_dict[key]["rel_weight"] = math.floor(((value["cprice"] * value["quantity"]) / total_value)*100)
            print(f"Total value of {value["stock_name"]} is {(value["cprice"] * value["quantity"])}\n")
            print(f"Relative weight of {value["stock_name"]} is {value['rel_weight']}%\n")

        name_list = []
        for key, value in stock_dict.items():
            name_list.append(value["stock_name"])

        print(name_list)
        
        rel_value_list = []
        for key, value in stock_dict.items():
            rel_value_list.append(value["rel_weight"])
        
        print(rel_value_list)

        y = np.array(rel_value_list)
        mylabels = list(name_list)


        plt.pie(y, labels = mylabels)
        plt.show()

    def run(self):
        # Read transactions from the CSV file
        transaction_dict = self.read_csv()

        # Get the current values of the stocks in the portfolio
        self.get_current_values(transaction_dict)

        # Plot the portfolio chart
        self.plot_portfolio_chart(transaction_dict)

## Main

mng = portfolio_manager()
if mng.ping('google.com'):
    print("Internet connection is active.")
    mng.run()
else:
    print("Internet connection is down.")

stock_dict = {}
stock_dict["VanEk defence"] = 33
stock_dict["Europe Stock 600"] = 67
mng.plot_portfolio_chart(stock_dict)
