import requests
from emoji import core
from io import BytesIO
import base64
from db import get_connection, create_tables, insert_character_category, insert_character_info
import time

start_time = time.time()
json = requests.get('https://api.wrtn.ai/be/characters?limit=100&sort=likeCount').json()
characters = json['data']['characters']

cnt_success = 0; cnt_fail = 0
connection = get_connection()
cursor = connection.cursor()
print("DB CONNECTED")
create_tables(cursor)

for index, character in enumerate(characters):
    character_category = character['categories'][0]['name']
    character_name = character['name']
    character_description = core.demojize(core.replace_emoji(character['description']))
    character_image = base64.b64encode(BytesIO(requests.get(character['profileImage']['origin']).content).getvalue())
    character_initialMessage = core.demojize(core.replace_emoji(character['initialMessages']))
    character_creator = character['creator']['nickname']

    insert_character_category(cursor, character_name, character_category)
    insert_character_info(
        cursor,
        character_name,
        character_description,
        character_image,
        character_initialMessage,
        character_creator
    )

    cnt_success += 1
    print(f'CHARACTER {index+1} SUCCESS')

print('API CRAWLING FINISHED')
end_time = time.time()
print(f'TOTAL TIME: {end_time - start_time:.2f}초')