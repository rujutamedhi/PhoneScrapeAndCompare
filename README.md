# Web Scraping App

An intelligent web scraping application designed to extract mobile data from popular e-commerce websites like Flipkart, Amazon, and Croma. The app provides functionality to sort and arrange the scraped mobile data by price in ascending or descending order. Additionally, it ensures real-time updates, reflecting any changes or new additions on the original websites.

---

## Features

- **Data Extraction**: Scrapes mobile details from Flipkart, Amazon, and Croma.
- **Real-Time Updates**: Automatically updates the mobile listings when the source websites are updated.
- **Sorting**: Allows sorting of mobiles based on price in ascending or descending order.

---

## Tech Stack

### Libraries & Frameworks
- **Beautiful Soup**: For extracting data from static HTML content.
- **Selenium**: For navigating URL.
- **Flask**: For building the backend logic and providing API endpoints.
- **HTML**: For structuring the web pages.
- **CSS**:For styling and making the interface visually appealing.
- **CSV**: For storing scraped data and managing persistent storage.

---

## Installation and Setup

Follow these steps to set up the project locally:

### Prerequisites
1. Python 3.10 or later
2. PostgreSQL installed on your system
3. WebDriver for Selenium (compatible with your browser)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/rujutamedhi/PhoneScrapeAndCompare
   
   ```
2. Configure Selenium:
   - Download the WebDriver for your browser (e.g., ChromeDriver for Chrome).
   - Ensure the WebDriver is in your system's PATH.

3. Run the scraping script to populate the database:
   ```bash
   python show.py
   ```


8. Open the app in your browser at `http://127.0.0.1:5000`.

---

## Usage

1. Use the search bar to search for specific mobile.
2. Use the sorting options to arrange mobiles in ascending or descending order based on price.
3. Check back regularly to see updated listings reflecting the latest data from the source websites.

---

## Future Enhancements

- Add more e-commerce platforms for data scraping.
- Implement advanced filtering options (e.g., brand, RAM, storage).
- Optimize scraping for faster performance.
- Create a user dashboard for personalized preferences.

