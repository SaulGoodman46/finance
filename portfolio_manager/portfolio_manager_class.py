import bs4
import requests
import sys
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

    def getFunds(self):
        file_name = "INPUTS/transactions.csv"
        
        print("Reading transactions.csv...\nPlease Wait")

        with open(file_name, "r") as csvfile:
            lines = csvfile.readlines()

        transaction_dict = {}
        first = 0
        for line in lines:
            strip_vect = line.strip(',')
            if (first == 0):
                first = 1
            elif (len(strip_vect) > 4):
                isin        = strip_vect[2]
                type        = strip_vect[0]
                stock_name  = strip_vect[1]
                date        = strip_vect[3]
                quantity    = strip_vect[4]
                value       = strip_vect[5]
                transaction_dict[isin] = [type, stock_name, date, quantity, value]

        print(isin, type, stock_name, date, quantity, value)

        url = 'https://markets.ft.com/data/funds/tearsheet/summary?s='


        #print(isin_codes)
        name_list = []
        price_list = []

        print("Getting Prices...\nPlease Wait")
        
        for isin in transaction_dict.keys():
            res = requests.get(url+ isin, headers={'User-Agent': 'Mozilla/5.0'})
            
            #Checking for Bad download
            try:
                res.raise_for_status()
            except Exception as exc:
                print("There was a problem: %s" % (exc))
            
            #making soup
            soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
            
            try:
                #if sys.argv[-2] =='-ft':
                name = soup_res.find('h1', {'class':'mod-tearsheet-overview__header__name mod-tearsheet-overview__header__name--large'})
                price = soup_res.find('span',{'class':'mod-ui-data-list__value'})
                #print(name.text,price.text)
                name_list.append(name.text)
                price_list.append(price.text.replace(',', ''))

                print(f"Found ISIN {isin}, called {name} with price {price}\n")

                #else:
                #    name = soup_res.find('a',{'class' : 'c-faceplate__company-link'})
                #    price = soup_res.find('span',{'class' : 'c-instrument c-instrument--last'})
                #    
                #    name_list.append(name.text.strip())
                #    price_list.append(''.join(price.text.split()))
                    
            except:
                name_list.append('NA')
                price_list.append('NA')
                continue
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
