from pymongo import MongoClient

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from typing import List, NamedTuple
username = "deneme"
password = "password_HERE"
client = MongoClient(f'mongodb+srv://deneme:(password_Here)@cluster0.zz9wxyc.mongodb.net/?retryWrites=true&w=majority')
db = client.ugurdmrer
pokemonCollection = db.pokemon


scrapedPokeData = []
class Pokemon(NamedTuple):
    poke_id: int
    pokeName: str
    pokeUrl: str
    pokeImage: str
    healthPower:int
    attackPower: int
    attackPower: int
    defencePower: int
    specialAttack: int
    specialDefence: int
    speed: int
    pokeTypes: List[str]

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
    pokeUrl = pokemonData[1].find_all('a')[0]['href']
    avatar = pokemonData[0].find_all("span")[0]
    healthPower = pokemonData[4].getText()
    attackPower = pokemonData[5].getText()
    defencePower = pokemonData[6].getText()
    specialAttack = pokemonData[7].getText()
    specialDefence = pokemonData[8].getText()
    speed = pokemonData[9].getText()
    for image in avatar:
        pokeImage = image['src']

# Catching types and store data in array
    pokeTypes= []
    for types in pokemonData[2].find_all("a"):
        pokeTypes.append(types.getText())
    
    # entryUrl = f'https://pokemondb.net{pokeUrl}'
    # request =Request(
    #     entryUrl,
    #     headers={'User-Agent': 'Mozilla/5.0'}
    # )
    # entryPageHtml = urlopen(request).read().decode('utf-8')
    # entrySoup = BeautifulSoup(entryPageHtml, "html.parser")
    
    typedPokemon = Pokemon(
        poke_id = int(poke_id),
        pokeName = str(pokeName),
        pokeUrl = pokeUrl,
        pokeImage = pokeImage,
        healthPower = int(healthPower),
        attackPower= int(attackPower),
        defencePower= int(defencePower),
        specialAttack=int(specialAttack),
        specialDefence=int(specialDefence),
        speed=int(speed),
        pokeTypes=pokeTypes
    )
    scrapedPokeData.append(typedPokemon)
    
    
    pokemonCollection.insert_one(
        {
            "id": typedPokemon.poke_id,
            "name": typedPokemon.pokeName,
            "image":typedPokemon.pokeImage,
            "types": typedPokemon.pokeTypes,
            "hp": typedPokemon.healthPower,
            "defense": typedPokemon.defencePower,
            "sp_attack": typedPokemon.specialAttack,
            "sp_defense": typedPokemon.specialDefence,
            "speed": typedPokemon.speed,
        }
    )