import requests
import re
from bs4 import BeautifulSoup

newproducts, knownproducts = [], []

with open('products.txt', 'r') as f:
    for line in f:
        knownproducts.append(line.strip())

#print(knownproducts)
        
page = requests.get('https://myshop.senecacollege.ca/collections/its-used-hardware-sale').content

soup = BeautifulSoup(page, 'lxml')

alla = soup.find_all(href=re.compile('.*\/collections\/its-used-hardware-sale.*'))
#print(alla)

#print(len(alla))

urls = [str(a)[str(a).find('href="') + 6 : str(a).find('"', str(a).find('href="')+6)] for a in alla]
urls = [url for url in urls if url.startswith('/collections') and not url.endswith('atom')]
#print(urls)

products = [url[url.rfind('/')+1:] for url in urls]
#print(products)


with open('products.txt', 'w') as f:
    for product in products:
        if product not in knownproducts:
            newproducts.append(product)
        f.write(product + '\n')

print(newproducts)
