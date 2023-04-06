import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.staples.com/Computer-office-desks/cat_CL210795/663ea?icid=BTS:2020:STUDYSPACE:DESKS"

try:
    response = requests.get(url)
    response.raise_for_status() # Check if there is an error in the response
except requests.exceptions.RequestException as e:
    print(e)
    exit(1)

soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('div', {'class': 'product-item'})

if len(products) == 0:
    print("No products found.")
else:
    product_list = []

    for product in products[:10]:
        title = product.find('a', {'class': 'product-title-link'})
        if title:
            title = title.text.strip()
        else:
            title = 'N/A'
        rating = product.find('span', {'class': 'seo-avg-rating'})
        if rating:
            rating = rating.text.strip()
        else:
            rating = 'N/A'
        reviews = product.find('span', {'class': 'seo-review-count'})
        if reviews:
            reviews = reviews.text.strip()
        else:
            reviews = 'N/A'
        price = product.find('span', {'class': 'price__large'})
        if price:
            price = price.text.strip()
        else:
            price = 'N/A'
        product_dict = {'Title': title, 'Rating': rating, 'Reviews': reviews, 'Price': price}
        product_list.append(product_dict)

    keys = product_list[0].keys()

    with open('top_10_products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(product_list)
