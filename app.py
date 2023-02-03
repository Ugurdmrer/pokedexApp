from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# Configure
url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
#Connection and read
page= urlopen(request)
pageContentBytes = page.read()

#Decode page, parse the page with soup
pageHtml = pageContentBytes.decode("utf-8")
soup = BeautifulSoup(pageHtml, "html.parser")

#Get pokedex rows
pokemonRows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")


#Loops for getting data's
for pokemon in pokemonRows:
    pokemonData = pokemon.find_all("td")
    poke_id = pokemonData[0]['data-sort-value']
    pokeName = pokemonData[1].find_all('a')[0].getText()
    avatar = pokemonData[0].find_all("span")[0]
    healthPower = pokemonData[4].getText()
    attackPower = pokemonData[5].getText()
    defencePower = pokemonData[6].getText()
    specialAttack = pokemonData[7].getText()
    specialDefence = pokemonData[8].getText()
    speed = pokemonData[9].getText()
    for image in avatar:
        pokeImage = image['src']

# Catching first type and check if there is second type or not
    pokeType1 = pokemonData[2].find_all('a')[0].getText()
    try:
        pokeType2 = pokemonData[2].find_all('a')[1].getText()
    except:
        continue
    