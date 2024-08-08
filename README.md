Google Maps Business Details Scraper
This Python script automates the process of extracting business details from Google Maps based on a list of search queries. It uses Selenium to interact with the Google Maps interface, allowing for automated data collection directly from the web.

Features
Automated Search: The script automatically searches for each query term on Google Maps.
Data Extraction: It extracts the following details:
Business Name
Business Category
Address
Website URL
Phone Number
Plus Code
Other available details
Error Handling: The script includes error handling to manage elements that might be missing or cause exceptions during scraping.
Logging: Errors and issues encountered during execution are logged for review.
Requirements
Python 3.x
Selenium
Google Chrome
ChromeDriver (compatible with your Chrome version)
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/pcb2k18/gmap-data-scraper.git
Navigate to the project directory:

bash
Copy code
cd gmaps_business_details_scrapper
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Download the ChromeDriver and place it in the specified directory in the script, or update the path in the script accordingly.

Usage
Place your search queries in a text file (e.g., search_queries.txt), with each query on a new line.

Run the script:

bash
Copy code
python app.py
The script will search for each query in Google Maps and extract the business details. Results will be saved to a file called gmap_results.txt in the same directory as your search queries file.

Any queries that fail to process after multiple attempts will be logged in failed_queries.txt.

Notes
The script includes a time.sleep() delay between operations to mimic human interaction and avoid potential issues with Google Maps.
The search results are written to a text file with each query result separated by a blank line for clarity.
Contributing
Feel free to submit issues or pull requests for improvements or new features.

License
This project is licensed under the MIT License. See the LICENSE file for details.
