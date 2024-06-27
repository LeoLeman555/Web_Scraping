import requests
from bs4 import BeautifulSoup

url = "http://www.scrapethissite.com/pages/simple/"

def get_text(element):
  if element:
    return element.text.strip()
  return None

response = requests.get(url)
response.encoding = response.apparent_encoding

countries_dict = {}

if response.status_code == 200:
  print(f"Connexion établie avec : {url}")
  html = response.text
  # Enregistrer le HTML localement
  with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

  soup = BeautifulSoup(html, "html5lib")
  # Exemple d'extraction de texte à partir d'un élément HTML
  countries = soup.find_all(class_='country')
  for country in countries:
    country_name = get_text(country.find(class_='country-name'))
    country_capital = get_text(country.find(class_='country-capital'))
    country_population = get_text(country.find(class_='country-population'))
    country_area = get_text(country.find(class_='country-area'))
    countries_dict[country_name] = {"Capital": country_capital, "Population": country_population, "Area": country_area}

else:
  print(f"ERREUR {response.status_code}: connexion non établie avec le site {url}")

# Demander à l'utilisateur quel pays il souhaite rechercher
country_to_find = input("Entrez le nom du pays que vous souhaitez rechercher : ")
if country_to_find in countries_dict:
  print(f"Informations sur {country_to_find} : {countries_dict[country_to_find]}")
else:
  print(f"Désolé, je n'ai pas trouvé d'informations sur {country_to_find}")

print("FIN")