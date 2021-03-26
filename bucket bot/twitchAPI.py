import json
import aiohttp
import asyncio
import toml

with open('config.toml', 'r') as ctoml:
    config = toml.load(ctoml)


async def refreshCode():
    
    url = "https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token="+config['twitch']['Refresh']+"&client_id=uqldoqgntkce4di5efwdsi88kzbryd&client_secret=xd24hvjlnzdud2npaul497s78lcnge"

    payload = {}
    headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                

                #response = requests.request("POST", url, headers=headers, data=payload)
                json = await response.json()
                token = json['access_token']
                refresh = json['refresh_token']
                config['twitch']['Code'] = token
                config['twitch']['Refresh'] = refresh
                with open('config.toml', 'w') as TomlFile:
                    toml.dump(config, TomlFile)
    finally:
        await session.close()


async def getLive():
    url = "https://api.twitch.tv/helix/search/channels?query=rustbucketgroup"

    payload={}
    headers = {
      'client-id': 'uqldoqgntkce4di5efwdsi88kzbryd',
      'Authorization': 'Bearer '+config['twitch']['Code']
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=payload, headers=headers) as response:
                #response = requests.request("GET", url, headers=headers, data=payload)
                return(await response.json())
    finally:
        await session.close()


async def getGame(id):
    url="https://api.twitch.tv/helix/games?id="+id
    payload={}
    headers = {
        'client-id': 'uqldoqgntkce4di5efwdsi88kzbryd',
        'Authorization': 'Bearer ' + config['twitch']['Code']
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=payload, headers=headers) as response:

        #response = requests.request("GET", url, headers=headers, data=payload)
                json = await response.json()
                return json['data'][0]['name']
    finally:
        await session.close()

async def getUsers():
    url="https://api.twitch.tv/helix/streams?user_login=rustbucketgroup"
    payload={}
    headers = {
        'client-id': 'uqldoqgntkce4di5efwdsi88kzbryd',
        'Authorization': 'Bearer ' + config['twitch']['Code']
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=payload, headers=headers) as response:

        #response = requests.request("GET", url, headers=headers, data=payload)
                json = await response.json()
                return json['data'][0]
    finally:
        await session.close()
