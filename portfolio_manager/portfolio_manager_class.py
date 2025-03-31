import bs4
import requests
import sys



class portfolio_manager:

    def getFunds(self):
        file_name = "INPUTS/transactions.csv"
        
        print("Reading transactions.csv...\nPlease Wait")

        with open(file_name, "r") as csvfile:
            lines = csvfile.readlines()

        transaction_dict = {}
        first = 0
        for line in lines:
            if (first == 0):
                first = 1
            else:
                strip_vect = line.strip(',')
                isin        = strip_vect[2]
                type        = strip_vect[0]
                stock_name  = strip_vect[1]
                date        = strip_vect[3]
                quantity    = strip_vect[4]
                value       = strip_vect[5]
                transaction_dict[isin] = [type, stock_name, date, quantity, value]

        if sys.argv[-2] =='-ft':
            url = 'https://markets.ft.com/data/funds/tearsheet/summary?s='
        else:
            url = 'https://www.boursorama.com/bourse/opcvm/cours/'


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


    def main(self):
        self.getFunds()

    if __name__=="__main__": 
        main()