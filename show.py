# 3.10.6 version

import csv
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, jsonify, request, render_template


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize Flask app
app = Flask(__name__)

# Path to your chromedriver
#service = Service("C:\chromedriver-win64\chromedriver.exe")
options = Options()
options.add_argument('--disable-web-security')
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')  # Uncomment if you need headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def update_data():
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        product_names = []
        prices = []
        descriptions = []
        reviews = []
        image_links = []
        details = []
        companylogo=[]
        logger.info("Navigating to the target URL")
        driver.get('https://www.smartprix.com/mobiles/price-below_60000/exclude_out_of_stock-exclude_upcoming-stock')
        print(driver.title)
        logger.info("Waiting for the grid container to be present")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.sm-products.list.size-m.img-long.len-20'))
        )
        logger.info("Element found")
        

        # Optional: Add a delay to observe the result
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "lxml")
        box = soup.find('div', class_='sm-products list size-m img-long len-20')
        
        if not box:
            raise Exception("The div with class 'sm-products' was not found on Smartprix")
        # company=box.find_all("img",class_='sm-img')
        # for com in company:
        #     src=com.get('src')
        #     companylogo.append(src if src else 'not available')
        # print(companylogo)
        # Extract prices
        price = box.find_all('span', class_='price')
        for p in price:
            prices.append(p.text if p else 'not available')

        # Extract product names
        name = box.find_all('div', class_='sm-product has-tag has-features has-actions')
        for n in name:
            names = n.find('h2')
            product_names.append(names.text if names else "not available")

        # Extract image links
        for n in name:
            link = n.find('img')
            href = link.get('src')
            image_links.append(href if href else "unavailable")

        # Extract descriptions
        des = box.find_all('ul', class_='sm-feat specs')
        uls = box.find_all('ul', class_='sm-feat specs')
        for ul in uls:
            list_items = ul.find_all('li')
            # Concatenate all <li> texts for this <ul>
            description_text = ' | '.join([li.text.strip() for li in list_items])
            descriptions.append(description_text if description_text else "not available")


        # Extract details links
        img_tag = box.find_all('a', class_='store')
        for img in img_tag:
            href = img.get('href')
            details.append(href if href else "Not available")
            reviews.append("unavailable")
            company=img.find("img",class_='sm-img')
            src=company.get('src')
            companylogo.append(src if src else 'not available')
        

        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()  # Make sure to close the driver

    # Create data dictionary
    new_data = {
        "Product Name": product_names,
        "Price": prices,
        "Description": descriptions,
        "Reviews": reviews,
        "Image Links": image_links,
        "Details": details,
        "Logo":companylogo
    }

    return pd.DataFrame(new_data)

# Initialize global data variable
data = pd.DataFrame()

# Route to serve the latest data in JSON format
@app.route('/latest_data')
def latest_data():
    global data
    return jsonify(data.to_dict(orient='records'))

# Route to refresh the data
@app.route('/refresh_data')
def refresh_data():
    global data
    new_data = update_data()
    if new_data is not None:
        data = new_data
        data.to_csv("finalmobile.csv", index=False, encoding='utf-8')

        return jsonify({"message": "Data refreshed successfully."})
    else:
        return jsonify({"error": "Failed to refresh data."})

# Route to sort data by price
@app.route('/sort_by_price', methods=['GET'])
def sort_by_price():
    order = request.args.get('order')
    global data
    if order == 'low':
        sorted_data = data.sort_values(by='Price', ascending=True)
    elif order == 'high':
        sorted_data = data.sort_values(by='Price', ascending=False)
    else:
        return jsonify({"error": "Invalid order."})
    return jsonify(sorted_data.to_dict(orient='records'))

# Route to sort data by site
@app.route('/sort_by_site', methods=['GET'])
def sort_by_site():
    site = request.args.get('site')
    global data
    if not site:
        return jsonify({'error': 'Site parameter is required'}), 400
    
    # Log the received site parameter
    logger.info(f"Filtering data by site: {site}")
    
    # Define a mapping from site names to logo links
    logo_links = {
        'Amazon': 'https://cdn1.smartprix.com/rx-iR2NxBi82-w32-h32/amazon.webp',
        'Chroma': 'https://cdn1.smartprix.com/rx-i4vfi1umq-w32-h32/croma.webp',
        'Flipkart': 'https://cdn1.smartprix.com/rx-i1jV84HS1-w32-h32/flipkart.webp'
    }
    
    # Check if the site parameter is valid
    if site not in logo_links:
        return jsonify({'error': 'Invalid site parameter'}), 400

    # Filter the data based on the logo link
    filtered_data = data[data['Logo'].str.contains(logo_links[site], case=False)]
    
    if filtered_data.empty:
        logger.info('No products found for the specified site.')
        return jsonify({'error': 'No products found for the specified site'}), 404
    
    return jsonify(filtered_data.to_dict(orient='records'))


# Route to search for products
@app.route('/search', methods=['POST'])
def search():
    global data
    search_query = request.form.get('searchQuery')
    # Filter the data based on the search query
    filtered_data = data[data['Product Name'].str.contains(search_query, case=False)]
    # Update the CSV file with the filtered data
    filtered_data.to_csv("finalmobile.csv", index=False)
    data = filtered_data
    print("Successful")
    return jsonify(filtered_data.to_dict(orient='records'))



# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=5002)

