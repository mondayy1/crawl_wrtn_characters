import os
import pymysql


def get_connection():
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "wrtn"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection


def create_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS character_category;')
    cursor.execute('DROP TABLE IF EXISTS character_info;')

    cursor.execute('''
        CREATE TABLE character_category (
            character_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(13),
            category VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE character_info (
            character_id INT AUTO_INCREMENT,
            name VARCHAR(13),
            description VARCHAR(251),
            imageBlob MEDIUMBLOB,
            initialMessage VARCHAR(1001),
            creator VARCHAR(13),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES character_category(character_id)
        ) ENGINE=MYISAM CHARSET=UTF8;
    ''')


def insert_character_category(cursor, name, category):
    query = '''
        INSERT INTO character_category (name, category)
        VALUES (%s, %s)
    '''
    cursor.execute(query, (name, category))


def insert_character_info(cursor, name, description, image_blob, initial_message, creator):
    """캐릭터 정보를 DB에 삽입"""
    query = '''
        INSERT INTO character_info (name, description, imageBlob, initialMessage, creator)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (name, description, image_blob, initial_message, creator))
