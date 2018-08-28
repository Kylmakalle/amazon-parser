import requests
import json
import math
from time import sleep
from bs4 import BeautifulSoup

# REVIEWS URL
PRODUCT_URL = 'https://www.amazon.com/dp/{product_id}'
PRODUCT_REVIEWS_URL_TEMPLATE = 'https://www.amazon.com/product-reviews/{product_id}/ie=UTF8&reviewerType=all_reviews'
REVIEW_URL_TEMPLATE = 'https://www.amazon.com/gp/customer-reviews/{review_id}'

BRANDS = [
    {'name': 'FitBark', 'product_id': ['B077MDJYKQ']},
    {'name': 'Garmin DeltaSmart', 'product_id': ['B01LICXOYW']},
    # {'name': 'Jagger & Lewis', 'product_id': ''},
    # {'name': 'Kippy', 'product_id': ''},
    # {'name': 'Kyon', 'product_id': ''},
    {'name': 'Link AKC', 'product_id': ['B01MFG7ELX']},
    # {'name': 'Nuzzle', 'product_id': ''},
    {'name': 'Paby', 'product_id': ['B0711V16N1']},
    # {'name': 'PawTrack', 'product_id': ''},
    {'name': 'PetPace', 'product_id': ['B01N4X6059']},
    {'name': 'PitPat', 'product_id': ['B0791M3D6V']},
    {'name': 'Poof (bean/pea)', 'product_id': ['B01K0VBOXU', 'B01K0UOMO4']},
    # {'name': 'Scollar', 'product_id': ['']},
    {'name': 'TabCat', 'product_id': ['B01FX7RDDG', 'B005N0PGVK']},
    {'name': 'TractiveGPS', 'product_id': ['B00F8A1ZBA', 'B072XMDHTZ']},
    {'name': 'TractiveMOTION', 'product_id': ['B00J2D8396']},
    {'name': 'Whistle', 'product_id': ['B01N7MWKWY']},
    {'name': 'WonderWoof', 'product_id': ['B00WKZG692']},
    # {'name': 'WUF', 'product_id': ['']}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def get_reviews_on_page(reviews_list):
    reviews_on_page = []
    for review in reviews_list:
        review_info = {}

        review_id = review['id']
        review_info['review_url'] = REVIEW_URL_TEMPLATE.format(review_id=review_id)

        review_info['title'] = review.find('a', {'data-hook': 'review-title'}).text
        review_info['stars'] = int(review.find('a', {'class': 'a-link-normal'})['title'][0])
        review_info['is_avp'] = bool(review.find('span', {'data-hook': 'avp-badge'}))

        helpful_for = review.find('span', {'data-hook': 'helpful-vote-statement'})
        if helpful_for is not None:
            helpful_for = helpful_for.text.split()[0]
            try:
                review_info['helpful_for'] = int(helpful_for.replace(',', ''))
            except ValueError:
                review_info['helpful_for'] = 1
        else:
            review_info['helpful_for'] = 0

        review_info['date'] = review.find('span', {'class': 'review-date'}).text[3:]
        review_info['text'] = review.find('span', {'data-hook': 'review-body'}).text
        reviews_on_page.append(review_info)
    return reviews_on_page


def get_reviews_by_item(item):
    result = []
    for product in item['product_id']:
        sleep(0.7)
        r = requests.get(PRODUCT_REVIEWS_URL_TEMPLATE.format(product_id=product) + '?pageSize=50', headers=HEADERS)
        print(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        total_reviews = int(soup.find('span', {'data-hook': 'total-review-count'}).text.replace(',', ''))
        total_pages = math.ceil(total_reviews / 50)
        reviews = soup.find('div', {'id': 'cm_cr-review_list'})
        reviews_list = reviews.find_all('div', {'class': 'a-section review'})

        item_reviews = get_reviews_on_page(reviews_list)

        if total_pages > 1:
            for page in range(2, total_pages + 1):
                sleep(0.7)
                r = requests.get(
                    PRODUCT_REVIEWS_URL_TEMPLATE.format(product_id=product) + '?pageNumber={}&pageSize=50'.format(page),
                    headers=HEADERS
                )
                print(r.url)
                soup = BeautifulSoup(r.text, "html.parser")
                reviews = soup.find('div', {'id': 'cm_cr-review_list'})
                reviews_list = reviews.find_all('div', {'class': 'a-section review'})
                item_reviews += get_reviews_on_page(reviews_list)

        result.append({
            'brand': item['name'],
            'url': PRODUCT_URL.format(product_id=product),
            'reviews': item_reviews
        })

    return result


DATA = []
for item in BRANDS:
    DATA += get_reviews_by_item(item)

with open('dump.json', 'w') as f:
    json.dump(DATA, indent=4, fp=f)
