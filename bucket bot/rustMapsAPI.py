import json
from mmap import MAP_SHARED
import aiohttp
import asyncio
import toml
import random

with open('config.toml', 'r') as ctoml:
    config = toml.load(ctoml)

async def getMaps():
    filterId = '8HMMM9N1fUe8dHLfmTNtWg'
    url = f"https://rustmaps.com/api/v2/maps/filter/{filterId}?page=1"

    payload = {}
    headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=payload, headers=headers) as response:
                randint = random.randint(0, 29)
                

                #response = requests.request("POST", url, headers=headers, data=payload)
                json = await response.json()
                maps = await getMap(json)
                mons = await getMonuments(maps)
                return mons, maps['url'], maps['imageIconUrl'] 
    finally:
        await session.close()

async def getMap(json):
    randint = random.randint(0, 29)
    url = f"https://rustmaps.com/api/v2/maps/{json['results'][randint]['id']}"

    payload = {}
    headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=payload, headers=headers) as response:
                randint = random.randint(0, 29)
                

                #response = requests.request("POST", url, headers=headers, data=payload)
                json = await response.json()
                return json
    finally:
        await session.close()

async def getMonuments(json):
    hasMons = []
    monuments = ['Airfield', 'Bandit_Town', 'Outpost', 'Excavator', 'Junkyard', 'Launch_Site', 'Military_Tunnels', 'Powerplant', 'Sewer_Branch', 'Sphere_Tank', 'Trainyard', 'Water_Treatment']
    monuments2 = json['monuments']
    for monu in monuments2:
        for mon in monuments:
            if monu['monument'] == mon:
                hasMons.append(mon)
    print(hasMons)
    return(hasMons)

