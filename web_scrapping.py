import requests
from bs4 import BeautifulSoup
import csv

def fetch_product_data(url, num_products=10):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_data = []
        product_tags = ["carpet","combination", "interior design", "beautiful", "color", "bed room"]
        for i, img in enumerate(soup.find_all('img')):
            if i >= num_products:
                break
            product_id = i + 1
            product_name = "carpet" + str(i) 
            category = "carpets"
            img_url = img.get('src')
            if img_url and img_url.startswith('http'):
                product_data.append((product_id, product_name, category, img_url, ", ".join(product_tags)))

        return product_data
    else:
        print(f"Error fetching URL: {response.status_code}")
        return []

def save_to_csv(product_data, file_name='product_data.csv'):
    with open(file_name, 'a+', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Product ID', 'Product Name', 'Category', 'Product Image Link', 'Product Tags'])
        for product in product_data:
            csvwriter.writerow(product)
    print(f"Product data successfully saved to {file_name}.")

if __name__ == "__main__":
    website_url = "https://www.google.com/search?q=carpets+for+bedroom&tbm=isch&ved=2ahUKEwi-vYKX4r-AAxURoekKHUIKClYQ2-cCegQIABAA&oq=carpets+for+&gs_lcp=CgNpbWcQARgBMgQIIxAnMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgYIABAHEB46BggAEAUQHlDSEVifIWCBM2gAcAB4AIABmAGIAbYMkgEEMC4xMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=bjzLZL7OLJHCpgfClKiwBQ&bih=554&biw=1226&hl=en-GB"
    num_products_to_fetch = 30
    product_data = fetch_product_data(website_url, num_products_to_fetch)
    save_to_csv(product_data, 'product_data.csv')
