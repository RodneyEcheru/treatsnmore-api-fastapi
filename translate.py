from fastapi import APIRouter, Form
from starlette.background import BackgroundTask

from sql import sql

import database
import re

# library to make http requests
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api = APIRouter(
    prefix="/translate",
    tags=["translate"],
    responses={404: {"message": "Request for a valid resource"}}
)


def insert_into_db(table, statement, data_type, values):
    database.orm(table, statement, data_type, values)


# async calls for french translations
async def api_translation(text: str, translation_language: str):
    from fastapi import BackgroundTasks

    # translation api
    url = f"https://api.mymemory.translated.net/get?q={text.strip()}&langpair=en|{translation_language.strip()}"

    # make api call
    response = requests.get(url, verify=False)  # make api call
    response = response.json()  # json decode response

    # if text is not translated, return text as is
    if not isinstance(response['matches'], list):
        return text

    # if text translation matches found, proceed

    # get translated text & strip tags from translation if any
    translation = re.sub("<.*?>", "", response["responseData"]["translatedText"])

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    values = {
        'language': 'en',
        'translationlanguage': 'fr',
        'text': text,
        'translation': translation,
    }
    statement = sql_statement.insert_into(table, values).sql_string

    # insert translation into database as using background task
    await database.orm_async(table, statement, 'list', values)
    # BackgroundTask(insert_into_db, table, statement, 'list', values)
    # background_tasks.add_task(insert_into_db, table, statement, 'list', values)
    # background_tasks = BackgroundTasks
    # background_tasks.add_task(insert_into_db, table, statement, 'list', values)

    return translation


def format_ip_address_to_proxy(current_ip_address: str):
    return {'https': f'http://{current_ip_address}'}


# async calls for french translations
async def api_translation_response(text: str, translation_language: str):
    import random

    # translation api
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{translation_language}"

    # make api call
    response = requests.get(url, verify=False)  # make api call
    response = response.json()  # json decode response

    # if text is not translated, return text as is
    if not isinstance(response['matches'], list):

        match_found = None

        # proxy list
        random_ip_addresses = [
            '149.56.86.231:80', '76.65.94.79:80', '68.183.111.90:80', '159.65.171.69:80', '157.230.84.252:80',
            '3.90.103.106:8080', '52.201.49.31:80', '142.116.32.230:80', '135.148.148.233:8080', '135.148.148.176:8080',
            '67.207.83.225:80', '67.55.74.5:5678', '167.172.141.70:14738', '51.222.12.245:10084',
            '68.183.111.220:12563',
            '3.12.95.129:80', '67.55.74.4:5678', '66.42.113.182:12345', '18.217.66.81:80', '167.71.249.173:40801',
            '198.199.86.148:36404', '12.186.206.83:80', '71.167.56.3:5678', '23.238.33.186:80', '207.210.47.61:5678',
            '162.243.244.206:80', '136.30.115.237:5678', '24.37.125.246:3629', '38.142.63.146:31596',
            '208.72.104.246:5678',
            '52.25.241.52:80', '65.126.149.35:5678', '159.65.225.8:24736', '70.82.75.118:4153', '64.121.5.186:5678',
            '50.233.103.190:80', '209.6.236.207:5678', '18.216.129.147:80', '3.101.73.214:80', '170.254.18.38:8888',
            '4.59.12.218:5678', '142.169.141.174:5678', '167.71.149.82:80', '213.156.136.88:5678', '70.60.96.154:5678',
            '38.113.171.108:5678', '74.143.245.221:80', '38.113.171.9:5678', '24.157.223.200:5678', '51.77.159.133:80',
            '71.13.85.122:5678', '173.36.197.60:80', '94.23.91.209:80', '24.37.245.42:51056', '50.127.81.50:5678',
            '188.165.226.99:80', '51.15.178.211:8118', '174.79.194.43:5678', '192.109.165.112:80', '193.149.225.29:80',
            '107.129.216.249:5678', '135.148.26.248:8080', '163.172.157.7:80', '51.195.76.214:3128',
            '8.211.241.63:1088',
            '18.134.240.88:80', '81.252.38.12:8080', '54.36.176.195:80', '80.82.215.6:80', '172.98.129.142:5678',
            '50.235.149.74:8080', '198.90.78.212:5678', '188.227.186.102:443', '98.188.123.90:5678', '51.210.243.0:80',
            '97.75.254.30:5678', '51.91.157.66:80', '8.211.241.7:1088', '193.149.225.7:80', '194.5.193.183:80',
            '69.70.41.188:5678', '185.170.215.228:80', '200.68.128.249:3128', '45.32.207.237:5678',
            '142.44.148.56:8080',
            '170.178.182.2:80', '137.74.65.101:80', '216.154.201.132:54321', '50.127.81.53:5678', '128.92.185.202:5678',
            '51.195.148.242:8080', '64.124.145.1:1080', '82.220.38.70:3128', '52.47.137.181:80', '96.3.212.186:5678',
            '148.66.38.230:5678', '38.100.66.26:5678', '74.94.194.3:1080', '167.172.155.178:25881',
            '207.154.205.135:9999',
            '67.212.98.183:5678', '147.194.190.186:5678', '100.19.135.109:80', '186.96.181.184:5678',
            '178.63.17.151:3128',
            '192.109.165.239:80', '73.31.207.254:5678', '97.75.254.13:5678', '138.0.231.14:5678', '45.5.92.225:5678',
            '67.22.223.9:39593', '50.212.252.97:5678', '24.15.196.187:5678', '51.68.141.31:80', '188.166.162.1:3128',
            '141.48.2.236:80', '206.145.26.94:5678', '51.195.203.253:80', '24.129.217.255:5678', '206.72.249.2:5678',
            '45.231.104.196:5678', '190.167.32.132:5678', '173.224.20.136:5678', '190.92.88.254:5678',
            '69.89.113.105:5678',
            '34.138.225.120:8888', '66.168.156.34:5678', '24.217.101.226:5678', '24.250.168.22:5678',
            '205.185.118.53:80',
            '24.139.143.226:4153', '8.26.226.30:5678', '68.12.146.250:5678', '71.95.92.61:5678', '70.171.60.35:5678',
            '68.39.224.160:5678', '162.219.43.238:5678', '97.83.39.182:5678', '181.114.25.58:5678',
            '181.210.30.138:5678',
            '97.87.172.0:5678', '173.246.49.116:5678', '24.37.221.246:4145', '66.172.112.181:5678',
            '199.127.176.139:64312',
            '75.188.33.94:5678', '207.210.47.34:5678', '181.189.230.194:5678', '152.70.222.244:3128',
            '70.185.68.155:4145',
            '20.76.164.205:3128', '68.183.111.90:80', '36.89.194.113:40252', '41.164.68.194:8080', '45.136.53.230:8080',
            '169.57.1.84:80', '103.12.160.85:31231', '47.245.33.104:12345', '170.83.60.125:55443', '62.252.146.74:8080',
            '161.202.226.194:80', '46.5.252.70:8080', '46.250.5.135:53281', '194.5.193.183:80', '12.186.206.83:80',
            '168.10.144.15:8080', '176.9.75.42:8080', '205.185.118.53:80', '185.170.215.228:80', '14.238.99.105:3128',
            '46.4.96.137:3128', '170.254.18.38:8888', '74.141.186.101:80', '35.189.22.187:80', '88.198.24.108:8080',
            '103.105.40.161:16538', '176.9.119.170:8080', '162.241.207.217:80', '157.230.84.252:80', '8.211.241.7:1088',
            '143.244.157.101:80', '158.46.127.222:52574', '118.163.94.3:80', '203.33.113.46:80', '50.233.103.190:80',
            '45.235.110.67:53281', '177.244.36.134:8080', '85.216.127.178:3128', '41.190.147.158:54018',
            '201.63.80.226:80', '82.64.183.22:8080', '46.237.255.4:8080', '82.212.62.27:8080', '173.246.129.9:80',
            '118.101.57.61:80', '201.81.38.93:8080', '14.252.206.21:55443', '159.203.61.169:8080', '167.71.5.83:8080',
            '47.242.183.4:8080', '36.92.22.70:8080', '178.215.175.34:8081', '200.115.53.193:3128', '203.142.71.52:8080',
            '103.14.198.105:83', '49.156.47.162:8080', '82.212.62.20:8080', '58.176.147.14:80', '3.101.73.214:80',
            '46.237.255.6:8080', '140.227.65.159:6000', '195.138.73.54:44017', '193.200.151.69:48241',
            '109.193.195.14:8080', '203.33.113.26:80', '168.196.211.10:55443', '149.172.255.10:8080',
            '52.78.172.171:80', '193.149.225.9:80', '36.67.27.189:39674', '46.5.252.53:8080', '207.244.227.169:443',
            '37.49.127.229:8080', '175.100.103.170:55443', '192.109.165.66:80', '41.234.66.33:3128',
            '82.212.62.23:8080', '149.172.255.13:3128', '91.89.89.11:8080', '46.5.252.58:8080', '210.220.67.60:8080',
            '213.230.127.139:3128', '119.81.189.194:80', '193.149.225.10:80', '193.149.225.103:80', '46.5.252.61:8080',
            '150.136.5.47:80', '203.33.113.98:80', '203.33.113.97:80', '88.198.50.103:8080', '210.2.135.253:3128',
            '149.172.255.11:8080', '187.243.253.2:8080', '187.94.61.248:80', '193.149.225.7:80', '182.253.0.44:808',
            '190.53.150.133:8118', '31.220.183.217:53281', '124.40.252.182:8080', '41.231.54.37:8888',
            '134.122.93.93:8080', '165.22.64.68:44153', '23.107.176.69:32180', '23.107.176.22:32180',
            '23.107.176.60:32180', '18.217.66.81:80', '23.107.176.116:32180', '23.107.176.24:32180',
            '116.90.229.186:35561', '200.85.169.18:47548', '36.94.133.138:8080', '203.33.113.243:80',
            '177.91.111.253:8080', '95.0.94.170:80', '195.209.131.19:46372', '124.219.176.139:39589',
            '115.42.8.15:53281', '52.149.152.236:80', '196.15.221.201:80', '34.87.84.105:80', '91.192.2.168:53281',
            '159.65.69.186:9300', '43.224.10.13:6666', '154.16.63.16:3128', '36.67.57.45:30066', '162.241.70.48:80',
            '85.216.127.182:8080', '109.193.195.13:8080', '41.79.191.182:80', '203.33.113.14:80', '170.106.175.94:80',
            '41.59.90.171:80', '190.63.169.34:53281', '118.97.47.249:55443', '20.88.192.37:3128',
            '138.121.216.129:8083', '37.1.22.6:53281', '36.66.239.114:8080', '189.80.3.187:8080', '186.159.3.193:56861',
            '191.7.201.109:52107', '194.233.69.41:443', '181.129.183.19:53281', '212.115.232.79:31280',
            '31.173.94.93:43539', '95.158.63.46:32923', '113.160.206.37:55138', '54.93.88.15:9300',
            '189.240.60.169:8080', '113.160.224.224:55443', '181.129.52.157:42648', '85.15.152.39:3128',
            '201.132.155.198:8080', '80.154.203.122:8080', '41.76.155.134:8080', '45.186.6.149:3128', '5.61.31.91:8081',
            '37.120.192.154:8080', '91.230.199.174:61440', '189.240.60.163:8080', '192.109.165.144:80',
            '85.216.127.188:8080', '196.15.221.205:80', '136.243.211.104:80', '186.219.96.47:54570', '37.59.22.27:8118',
            '194.163.132.232:3128', '197.210.217.66:34808', '183.91.0.120:3128', '216.169.73.65:34679',
            '91.218.244.153:8080', '85.159.48.170:40014', '124.41.240.96:55443', '181.129.140.83:35232',
            '34.138.225.120:8888', '169.239.188.61:48807', '200.25.254.193:54240', '213.230.90.106:3128',
            '162.247.181.118:8080', '169.57.1.85:8123', '213.230.97.169:3128', '109.120.209.67:8118',
            '189.240.60.168:8080', '212.22.169.22:8085', '197.81.195.200:8080', '187.44.230.86:3128',
            '125.62.198.65:83', '45.179.184.6:8083', '202.29.6.226:8080', '89.163.158.206:8080', '51.38.99.136:3128',
            '61.7.138.48:8080', '118.97.164.19:8080', '110.76.148.242:8080', '77.119.250.129:8080',
            '200.89.178.159:3128', '180.183.67.229:8080', '3.88.248.151:80', '210.186.175.180:80',
            '178.128.108.108:8118', '202.40.188.90:40486', '103.92.114.6:8080', '61.219.53.23:80', '79.143.87.134:9090',
            '3.221.190.166:8118', '103.4.66.165:55443', '37.187.114.131:80', '167.71.212.154:80', '200.185.55.121:9090',
            '173.82.116.186:80', '51.75.206.209:80', '79.111.13.155:50625', '82.99.232.18:58689', '178.151.34.43:8080',
            '213.157.51.210:53227', '14.102.44.25:44047', '110.238.116.69:12345', '88.82.95.146:3128',
            '37.57.15.43:33761', '159.138.253.116:12345', '210.14.35.194:55443', '182.72.150.242:8080',
            '89.222.182.144:3128', '47.243.23.114:8080', '150.129.171.123:6666', '31.40.146.179:53281',
            '96.9.74.91:8080', '54.242.70.230:80', '36.89.229.97:59707', '197.155.158.22:80', '114.32.84.229:8080',
            '221.125.138.189:8380', '175.139.179.65:42580', '87.237.234.187:3128', '160.251.19.21:8118',
            '1.179.183.73:50178', '103.253.146.90:80', '181.49.100.190:8080', '122.15.131.65:57873',
            '195.158.7.10:3128', '213.32.75.44:9300', '188.190.245.135:55443', '114.199.198.211:8080',
            '192.109.165.101:80', '5.149.219.201:8080', '59.153.17.186:53281', '3.217.181.204:80', '172.105.40.232:80',
            '200.136.74.233:8080', '176.98.75.229:54256', '203.33.113.200:80', '178.217.172.206:55443',
            '41.59.90.92:80', '170.82.118.89:8083', '51.68.141.31:80', '47.74.18.244:80', '203.33.113.233:80',
            '150.107.207.137:61954', '109.105.205.232:59152', '178.128.243.15:80', '203.33.113.248:80',
            '37.44.247.93:80', '46.237.255.11:8080', '18.132.18.81:80', '43.255.113.232:80', '64.225.49.147:80',
            '158.177.253.24:80', '159.65.171.69:80', '118.179.173.253:40836', '85.214.83.135:8085', '212.227.11.61:80',
            '85.216.127.190:8080', '79.143.87.117:9090', '191.96.42.80:8080', '202.70.67.93:80', '123.25.25.230:4002',
            '152.231.29.37:18080', '169.239.182.135:80', '46.146.239.100:3128', '161.117.89.36:8888', '14.97.2.108:80',
            '185.56.209.114:52342', '62.210.177.105:3128', '36.37.139.2:43997', '187.216.93.20:55443',
            '187.111.176.62:8080', '203.33.113.190:80', '178.254.42.75:80', '50.246.120.125:8080',
            '202.169.229.139:53281', '75.188.225.212:8080', '203.33.113.221:80', '192.109.165.81:80',
            '102.140.113.202:55443', '192.109.165.239:80', '157.90.141.221:80', '170.82.118.221:8083',
            '203.33.113.112:80', '89.250.149.114:60981', '51.81.82.175:80'
        ]

        while match_found is None and len(random_ip_addresses) != 0:
            current_ip_address = random.choice(random_ip_addresses)
            while current_ip_address in random_ip_addresses:
                random_ip_addresses.remove(current_ip_address)
            proxy_address = format_ip_address_to_proxy(current_ip_address)

            # make api call
            response = requests.get(url, proxies=proxy_address, verify=False)
            response = response.json()  # json decode response

            if isinstance(response['matches'], list):
                match_found = True

        if not isinstance(response['matches'], list):
            return None

    # if text translation matches found, proceed

    # get translated text & strip tags from translation if any
    translation = re.sub("<.*?>", "", response["responseData"]["translatedText"])

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    values = {
        'language': 'en',
        'translationlanguage': 'fr',
        'text': text,
        'translation': translation,
    }
    statement = sql_statement.insert_into(table, values).sql_string

    # insert translation into database as using background task
    # await database.orm_async(table, statement, 'list')
    BackgroundTasks.add_task(database.orm, table, statement, 'dictionary', values)
    return translation


# async calls for french translations
async def api_proxy_translation_response(text: str, translation_language: str):
    # translation api
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{translation_language}"

    # make api call
    response = requests.get(url, verify=False)  # make api call
    response = response.json()  # json decode response

    # if text is not translated, try proxies
    if not isinstance(response['matches'], list):
        return None

    # if text translation matches found, proceed

    # get translated text & strip tags from translation if any
    translation = re.sub("<.*?>", "", response["responseData"]["translatedText"])

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    values = {
        'language': 'en',
        'translationlanguage': 'fr',
        'text': text,
        'translation': translation,
    }
    statement = sql_statement.insert_into(table, values).sql_string

    # insert translation into database as using background task
    await database.orm_async(table, statement, 'list')
    # BackgroundTasks.add_task(database.orm, table, statement, 'dictionary', values)
    return translation


# async calls for french translations
async def api_translation_response_bk(url: str, text: str):
    # make api call
    response = requests.get(url, verify=False)  # make api call
    response = response.json()  # json decode response

    # if text is not translated, return text as is
    if not isinstance(response['matches'], list):
        return None

    # if text translation matches found, proceed

    # get translated text & strip tags from translation if any
    translation = re.sub("<.*?>", "", response["responseData"]["translatedText"])

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    values = {
        'language': 'en',
        'translationlanguage': 'fr',
        'text': text,
        'translation': translation,
    }
    statement = sql_statement.insert_into(table, values).sql_string

    # insert translation into database as using background task
    await database.orm_async(table, statement, 'list')
    # BackgroundTasks.add_task(database.orm, table, statement, 'dictionary', values)
    return translation


# translate languages using api from mymemory
def translate(current_language: str, translation_language: str, current_text: str):
    # check if translation exists in database

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    statement = sql_statement.select(table).where().id('translationlanguage', translation_language).and_().id('text',
                                                                                                              current_text).sql_string

    results = database.orm(table, statement, 'dictionary')

    if results is None:
        url = "https://api.mymemory.translated.net/get?q=" + current_text + "&langpair=" + current_language + "|" + translation_language
        response = requests.get(url, verify=False)  # make api call
        response = response.json()  # json decode response
        if 'translatedText' in response["responseData"]:
            translation = response["responseData"]["translatedText"]  # get translated text

            # generate sql string
            sql_statement = sql()
            table = 'translations'
            values = {
                'language': current_language,
                'translationlanguage': translation_language,
                'text': current_text,
                'translation': translation,
            }
            statement = sql_statement.insert_into(table, values).sql_string

            # insert translation into database as using background task
            BackgroundTasks.add_task(database.orm, table, statement, 'dictionary', values)

            results = translation

        else:
            results = current_text

    else:
        results = results['translation']

    return results  # return translation


# translate languages using api from mymemory
async def translate_all(translation_language: str, array: list):
    # get all translations in database

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    statement = sql_statement.select(table).sql_string

    database_translations = database.orm(table, statement, 'list')

    if database_translations is None:

        list_items = 0

        # Iterating using while loop
        while list_items < len(array):

            for key, value in array[list_items].items():

                translated_text = await api_translation_response(array[list_items][value], translation_language)
                if translated_text is None:  # stop translating once translation limit is reached
                    return array

                array[list_items][key] = translated_text

            list_items += 1

    else:

        list_items = 0

        # Iterating using while loop
        while list_items < len(array):

            for key, value in array[list_items].items():

                # loop through database translation

                # Iterating using while loop
                translation_found = False
                database_items = 0

                while database_items < len(database_translations) and translation_found is not True:

                    for database_item in database_translations:
                        if array[list_items][key] == database_item['text']:
                            array[list_items][key] = database_item['translation']
                            translation_found = True

                        database_items += 1

                if translation_found is False:
                    query = array[list_items][key].strip()

                    translated_text = await api_translation(query, translation_language)

                    # translated_text = await api_translation_response(url, array[list_items][value])
                    # translated_text = await api_translation_response(url, array[list_items][value])

                    array[list_items][key] = translated_text

            list_items += 1

    return array  # return translations


# translate languages using api from mymemory
async def translate_all_bk(translation_language: str, array: list):
    # get all translations in database

    # generate sql string
    sql_statement = sql()
    table = 'translations'
    statement = sql_statement.select(table).sql_string

    database_translations = database.orm(table, statement, 'list')

    if database_translations is None:

        list_items = 0

        # Iterating using while loop
        while list_items < len(array):

            for key, value in array[list_items].items():

                translated_text = await api_translation_response(array[list_items][value], translation_language)
                if translated_text is None:  # stop translating once translation limit is reached
                    return array

                array[list_items][key] = translated_text

            list_items += 1

    else:

        list_items = 0

        # Iterating using while loop
        while list_items < len(array):

            for key, value in array[list_items].items():

                # loop through database translation

                # Iterating using while loop
                translation_found = False
                database_items = 0

                while database_items < len(database_translations) and translation_found is not True:

                    for database_item in database_translations:
                        if array[list_items][key] == database_item['text']:
                            array[list_items][key] = database_item['translation']
                            translation_found = True

                        database_items += 1

                if translation_found is False:
                    query = array[list_items][key].strip()

                    url = "https://api.mymemory.translated.net/get?q=" + query + "&langpair=en|" + translation_language

                    translated_text = await api_proxy_translation_response(query, translation_language)

                    # translated_text = await api_translation_response(url, array[list_items][value])
                    # translated_text = await api_translation_response(url, array[list_items][value])
                    if translated_text is None:  # stop translating once translation limit is reached
                        return array

                    array[list_items][key] = translated_text

            list_items += 1

    return array  # return translations


# translate list
async def translate_array(translation_language: str, array: list):
    # translate text

    return await translate_all(translation_language, array)


# translate post request
@api.post("/{current_language}/{translation_language}")
def translationroute(current_language: str, translation_language: str, text: str = Form(...)):
    # translate text

    return translate(current_language, translation_language, text)


# translate post request array
@api.post("/{translation_language}")
async def translationroutearray(translation_language: str, array=Form(...)):
    # translate text

    return await translate_all(translation_language, array)


@api.get("/")
def welcome():
    return {
        "message": "You have reached translate endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }
