from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from io import BytesIO
import base64
from emoji import core
import time


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
  
    driver = webdriver.Chrome(options=options)

    driver.get('https://wrtn.ai/character/explore?sort=likeCount')
    time.sleep(2)
    return driver


def fetch_character_data(driver, category_index, character_index):
    wait = WebDriverWait(driver, 10)
    
    if category_index >= 9: # 카테고리 이동
        category_expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="character-explore-scroll"]/div/div/div[3]/div/div[2]/button')))
        category_expand_button.click()
        time.sleep(1)

    # 카테고리 선택
    character_category_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="character-explore-scroll"]/div/div/div[3]/div/div/div/div[{category_index}]')
        )
    )
    character_category = character_category_button.text
    character_category_button.click()
    time.sleep(1)
    
    # 캐릭터 선택 및 데이터 추출
    character_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'[data-index="{character_index}"]')
        )
    )
    elements = character_element.text.splitlines()
    img_tag = character_element.find_element(By.TAG_NAME, 'img')
    character_image_url = img_tag.get_attribute('src')
    
    # 캐릭터 이미지, 이름, 설명 등 데이터 추출
    character_image_blob = base64.b64encode(BytesIO(requests.get(character_image_url).content).getvalue())
    character_name = elements[0]
    character_description = ' ' if len(elements) <= 2 else core.demojize(core.replace_emoji(elements[1], ""))
    character_creator = elements[-1]
    
    # 초기 메시지 추출
    character_element.click()
    character_chat_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="web-modal"]/div/div/div/div[4]/button')))
    character_chat_button.click()
    try:
        character_chat = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="chat-content"]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]/div')))
        character_initial_message = core.demojize(core.replace_emoji(character_chat.text, ""))
    except:
        character_initial_message = ''
    
    return {
        "name": character_name,
        "description": character_description,
        "image_blob": character_image_blob,
        "initial_message": character_initial_message,
        "creator": character_creator,
        "category": character_category
    }
