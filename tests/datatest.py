from io import BytesIO
from PIL import Image
import base64
import pymysql
import os

def checkRecordCounts(cursor):
    cursor.execute("SELECT COUNT(*) FROM character_category")
    category_count = cursor.fetchone()['COUNT(*)']
    cursor.execute("SELECT COUNT(*) FROM character_info")
    info_count = cursor.fetchone()['COUNT(*)']
    if category_count == 100 and info_count == 100:
        print("checkRecordCount SUCCESS")
    else:
        print(f"checkRecordCount FAILED, category has {category_count}, info has {info_count}")

def checkDuplicated(cursor):
    cursor.execute("SELECT name, description, initialMessage, COUNT(*) FROM character_info GROUP BY name, description, initialMessage HAVING COUNT(*) > 1")
    info_duplicates = cursor.fetchall()
    if not info_duplicates:
        print("checkDuplicted SUCCESS")
    else:
        print("checkDuplicated FAILED, character_info")

def checkNULLValues(cursor):
    cursor.execute("SELECT COUNT(*) FROM character_category WHERE name IS NULL")
    category_null_count = cursor.fetchone()['COUNT(*)']
    cursor.execute("SELECT COUNT(*) FROM character_info WHERE name IS NULL")
    info_null_count = cursor.fetchone()['COUNT(*)']
    if category_null_count == 0 and info_null_count == 0:
        print("checkNULLValues SUCCESS")
    else:
        print(f"checkNULLValues FAILED, category has {category_null_count}, info has {info_null_count}")

def checkInfo(cursor):
    cursor.execute("SELECT * FROM character_info ORDER BY rand() LIMIT 1")
    result = cursor.fetchone()
    image_blob = result.pop('imageBlob')
    image_data = base64.b64decode(image_blob)
    image = Image.open(BytesIO(image_data))
    #image.show()
    image.save("character_img.png")
    print(result)
    print("Manually check Image and stuffs...")

if __name__ == "__main__":
    connection = pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "wrtn"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    cursor = connection.cursor()

    checkRecordCounts(cursor)
    checkDuplicated(cursor)
    checkNULLValues(cursor)
    checkInfo(cursor)
    
    cursor.close()
    connection.close()