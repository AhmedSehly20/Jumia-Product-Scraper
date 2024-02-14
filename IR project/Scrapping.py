#to call out the page
import requests
#parsing the file to extract the data and analyze the text
from bs4 import BeautifulSoup
import csv
import os.path

def scrape_jumia_product(url):
    #get the url webstite
    response = requests.get(url)
    #used lxml because it's faster and more compatible than html.parser
    #get the content of the website
    soup = BeautifulSoup(response.content, 'lxml')

    product_page = url
#get the product name
    product_name_element = soup.find('h1', class_='-fs20 -pts -pbxs')
    #get the text and use strip remove the spaces
    product_name = product_name_element.text.strip() if product_name_element else "N/A"
#get the range
    price_range_element = soup.find('span', class_='-b -ltr -tal -fs24')
    price_range = price_range_element.text.strip() if price_range_element else "N/A"
#get the ratings
    ratings_element = soup.find('div', class_='stars')
    ratings = ratings_element.text.strip() if ratings_element else "N/A"
#we copied all of the div contnet and then get it by index
    company_name_element = soup.find_all('div', class_="-pvxs")
    company_name = company_name_element[1].find('a').text.strip() if len(company_name_element) > 1 else "N/A"
#get the product image
    product_image_element = soup.find('img', class_='-fw -fh')
    product_image = product_image_element['data-src'] if product_image_element else "N/A"
#printing
    print("Product Page:", product_page)
    print("Product Name:", product_name)
    print("Price Range / Price:", price_range)
    print("Ratings:", ratings)
    print("Company Name:", company_name)
    print("Product Image URL:", product_image)
 #make a list of the fields
#make it easier to access
    return {'Product Page': product_page,
            'Product Name': product_name,
            'Price Range / Price': price_range,
            'Ratings': ratings,
            'Company Name': company_name,
            'Product Image URL': product_image}



def save_product_to_csv(product_data):
    fieldnames = ['Product Page', 'Product Name', 'Price Range / Price', 'Ratings', 'Company Name', 'Product Image URL']

    with open('jumia_product.csv', 'a', newline='', encoding='utf-8-sig', errors='ignore') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty, then write the header
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(product_data)

    print("Data saved successfully!")

#calling the functions
product_url = "https://www.jumia.com.eg/redragon-m711-cobra-rgb-gaming-mouse-10000-dpi-7-mmo-buttons-15048664.html"
product_data = scrape_jumia_product(product_url)
save_product_to_csv(product_data)