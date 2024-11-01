FROM ubuntu

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치
RUN apt update && \
    apt install -y wget unzip nano python3 curl default-mysql-client

# python 명령어 심볼릭 링크 추가
RUN ln -s /usr/bin/python3 /usr/bin/python

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 프로젝트 파일 복사
COPY . /app

# Poetry로 Python 패키지 설치
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Keep the container running
CMD ["tail", "-f", "/dev/null"]

#poetry run python ./myproject/apicrawl_with_run.py
