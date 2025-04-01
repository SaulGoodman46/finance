import yfinance as yf
import subprocess
import platform
import matplotlib.pyplot as plt
import numpy as np

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

        with open(file_name, "r") as csvfile:
            lines = csvfile.readlines()

        transaction_dict = {}
        first = 0
        for line in lines:
            strip_vect = line.strip(',')
            tmp_dict = {}
            if (first == 0):
                first = 1
            elif (len(strip_vect) > 4):
                ticker        = strip_vect[2]
                tmp_dict["type"]        = strip_vect[0]
                tmp_dict["stock_name"]  = strip_vect[1]
                tmp_dict["date"]        = strip_vect[3]
                tmp_dict["quantity"]    = strip_vect[4]
                tmp_dict["value"]       = strip_vect[5]
                transaction_dict[ticker] = tmp_dict

                print(f"Loaded ticker {ticker} with values {tmp_dict[ticker]}")

        return transaction_dict
    
    def get_stock_price_by_ticker(ticker):
        if not ticker:
            raise ValueError(f"Ticker not found: {ticker}")

        # Recupera i dati dell'azione utilizzando il ticker
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        current_price = stock_info.get('currentPrice')

        if current_price is None:
            raise ValueError(f"Prezzo non disponibile per il ticker: {ticker}")

        return current_price

    def get_current_values(self, stock_dict):
        for key in stock_dict.keys():
            tmp_dict = stock_dict[key]

            
            print(f"Ticker: {key} found value {self.get_stock_price_by_ticker(key)}")
            
            tmp_dict["cprice"] = self.get_stock_price_by_ticker(key)
            tmp_dict["cvalue"] = tmp_dict["cprice"] * tmp_dict["quantity"]
            tmp_dict["profit"] = tmp_dict["cvalue"] - (tmp_dict["value"] * tmp_dict["quantity"])

            stock_dict[key] = tmp_dict


    def plot_portfolio_chart(self, stock_dict):
        
        
        y = np.array(list(stock_dict.values()))
        mylabels = list(stock_dict.keys())


        plt.pie(y, labels = mylabels)
        plt.show() 

## Main

mng = portfolio_manager()
if mng.ping('google.com'):
    print("Internet connection is active.")
    mng.getFunds()
else:
    print("Internet connection is down.")

stock_dict = {}
stock_dict["VanEk defence"] = 33
stock_dict["Europe Stock 600"] = 67
mng.plot_portfolio_chart(stock_dict)
