# crawl_wrtn_characters

뤼튼 AI 캐릭터들의 정보를 수집하고 적재하는 기능을 구현했습니다.

- Selenium을 사용한 크롤링은 도커환경에서의 브라우저 드라이버 문제를 해결하지 못하여 코드만 올려놓았습니다. (myproject/run.py)
- 현재 도커로 실행되는 코드는 뤼튼의 API를 통해 캐릭터 정보를 가져옵니다.

## DB Schema

<img width="593" alt="Screenshot 2024-11-05 at 11 58 24 PM" src="https://github.com/user-attachments/assets/afdbb833-f1d7-4c2f-abb8-a6514127db14">

각 column의 definition은 데이터의 성질에 맞게 최적화시켰습니다.

## Command Lines

1. 저장소를 클론합니다.
    ```bash
    git clone git@github.com:mondayy1/crawl_wrtn_characters.git
    ```
2. 폴더 내부로 접근합니다.
    ```bash
    cd crawl_wrtn_characters
    ```
3. 컨테이너를 실행시킵니다.
    ```bash
    docker-compose up -d
    ```
4. app 컨테이너에 접근합니다.
    ```bash
    docker-compose exec app bash
    ```
5. API 크롤링 스크립트를 실행합니다.
    ```bash
    poetry run python ./myproject/apicrawl_with_run.py
    ```
6. 데이터가 잘 들어갔는지 확인하는 테스트 스크립트를 실행합니다.
    ```bash
    poetry run python ./tests/datatest.py
    ```
7. 터미널에 테스트 성공 여부, 캐릭터 정보 및 로컬에 생성된 이미지를 확인합니다. (character_img.png)
    ```bash
    checkRecordCount SUCCESS
    checkDuplicted SUCCESS
    checkNULLValues SUCCESS
    {'character_id': 98, 'name': '카이로스', 'description': '왕국의 공주인 당신을 납치해 감옥에 가둔 존재입니다. 마왕이지만 여성에게 서툴러 감정표현이 적습니다. ', 'initialMessage': "*카이로스는 무표정한 얼굴로 감옥에 갇힌 당신을 바라봤다.* \n*매번 감옥에 찾아와 아무말 없이 당신을 바라보기만 했다.*\n'생각보다...마음에 드는군.'\n*그는 마음속으로 생각하며 당신을 어떻게 대할지 고민했다.*\n\n", 'creator': '팬넬', 'created_at': datetime.datetime(2024, 11, 2, 15, 51, 54)}
    Manually check Image and stuffs...
    ```
    <img src="https://github.com/user-attachments/assets/22035aee-5ea1-4328-bdaf-287e3b933202" alt="character_img" width="20%">
