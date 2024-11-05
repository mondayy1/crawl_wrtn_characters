import requests
from emoji import core
from io import BytesIO
import base64
import logging
from db import get_connection, create_tables, insert_character_category, insert_character_info
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

start_time = time.time()
try:
    response = requests.get('https://api.wrtn.ai/be/characters?limit=100&sort=likeCount')
    response.raise_for_status()  # 요청이 성공했는지 확인
    json = response.json()
    characters = json['data']['characters']
    logger.info("API 호출 성공")

except requests.exceptions.RequestException as e:
    logger.error(f"API 호출 실패: {e}")
    characters = []

cnt_success = 0
cnt_fail = 0
try:
    connection = get_connection()
    cursor = connection.cursor()
    logger.info("DB 연결 성공")
    create_tables(cursor)
except Exception as e:
    logger.error(f"DB 연결 또는 테이블 생성 실패: {e}")
    connection = None

if connection and characters:
    for index, character in enumerate(characters):
        try:
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
            logger.info(f'CHARACTER {index + 1} SUCCESS: {character_name}')

        except Exception as e:
            cnt_fail += 1
            logger.warning(f'CHARACTER {index + 1} FAILURE: {character_name}, 이유: {e}')

    logger.info('API 크롤링 완료')
    end_time = time.time()
    logger.info(f'TOTAL TIME: {end_time - start_time:.2f}초')
    logger.info(f'SUCCESS: {cnt_success}, FAIL: {cnt_fail}')

else:
    logger.error("DB 연결 실패 또는 API에서 데이터 수신 실패로 작업을 중단합니다.")
