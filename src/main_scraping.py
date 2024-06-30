import requests
from bs4 import BeautifulSoup
import os

# URL of the site to scrape
URL = "http://www.scrapethissite.com/pages/simple/"
# Path of the file where the HTML will be saved
FILE_PATH = "src/index.html"

def extract_text_from_element(element):
    """
    Extracts the text from a BeautifulSoup element, removing any excess whitespace.
    If the element is None, returns None.
    """
    return element.text.strip() if element else None

def delete_file(file_path):
    """
    Deletes a file at the given path.
    """
    os.remove(file_path)

def fetch_html(url):
    """
    Fetches the HTML content from the given URL using a GET request.
    If the request is successful, returns the HTML as a string.
    If the request fails, prints an error message and returns None.
    """
    with requests.get(url) as response:
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            print(f"Connection established with: {url}")
            return response.text
        else:
            print(f"ERROR {response.status_code}: connection not established with the site {url}")
            return None

def parse_html(html):
    """
    Parses the given HTML using BeautifulSoup and extracts information about countries.
    Returns a dictionary where the keys are country names and the values are dictionaries
    with information about the country's capital, population, and area.
    """
    soup = BeautifulSoup(html, "html5lib")
    countries = soup.find_all(class_='country')
    return {
        extract_text_from_element(country.find(class_='country-name')): {
            "Capital": extract_text_from_element(country.find(class_='country-capital')),
            "Population": extract_text_from_element(country.find(class_='country-population')),
            "Area": extract_text_from_element(country.find(class_='country-area'))
        } for country in countries
    }

def interact_with_user(countries_dict):
    """
    Interacts with the user, asking them to input a country name.
    If the country is in the dictionary, prints information about the country.
    If the country is not in the dictionary, prints an error message.
    """
    country_to_find = str.capitalize(input("Enter the name of the country you want to search for: "))
    if country_to_find in countries_dict:
        print(f"Information about {country_to_find} : {countries_dict[country_to_find]}")
    else:
        print(f"Sorry, I couldn't find any information about {country_to_find}")

def main():
    """
    Main function that orchestrates the scraping process.
    Fetches the HTML from the URL, parses it to extract country information,
    interacts with the user, and then deletes the saved HTML file.
    """
    html = fetch_html(URL)
    if html:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        countries_dict = parse_html(html)
        interact_with_user(countries_dict)
        delete_file(FILE_PATH)
    print("END")

if __name__ == "__main__":
    main()