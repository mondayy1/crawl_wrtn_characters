import logging
import time
from db import get_connection, create_tables, insert_character_category, insert_character_info
from crawler import init_driver, fetch_character_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main(cnt_character):
    start_time = time.time()
    cnt_success = 0; cnt_fail = 0
    connection = get_connection()
    cursor = connection.cursor()
    logger.info("DB CONNECTED")
    
    create_tables(cursor)
    
    driver = init_driver()
    logger.info("WEB DRIVER INITIATED")
    
    for category_index in range(2, 12): # 로맨스(2) ~
        for character_index in range(cnt_character):
            attempts = 0
            success = False
            while attempts < 10 and not success:
                try:
                    data = fetch_character_data(driver, category_index, character_index)
                    success = True
                except:
                    driver.get('https://wrtn.ai/character/explore?sort=likeCount')
                    attempts += 1
                    logger.warning(f"Retry {attempts} for CATEGORY {category_index-1} / CHARACTER {character_index+1}")
                    time.sleep(1)
                    
            if success:
                insert_character_category(cursor, data["name"], data["category"])
                insert_character_info(
                    cursor,
                    data["name"],
                    data["description"],
                    data["image_blob"],
                    data["initial_message"],
                    data["creator"]
                )
                driver.back()
                time.sleep(1)
                cnt_success += 1
                logger.info(f'CATEGORY {category_index-1} / CHARACTER {character_index+1} SUCCESS')
            else:
                cnt_fail += 1
                logger.warning(f'CATEGORY {category_index-1} / CHARACTER {character_index+1} FAILED AFTER 10 ATTEMPTS')
    logger.info('CRAWLING FINISHED')
    
    driver.quit()
    connection.close()
    end_time = time.time()
    logger.info(f'TOTAL TIME: {end_time - start_time:.2f}초')
    logger.info(f'GET {cnt_success+cnt_fail} CHARACTERS, SUCCESS:{cnt_success} FAIL:{cnt_fail}')

if __name__ == "__main__":
    cnt_character = 10
    main(cnt_character)
