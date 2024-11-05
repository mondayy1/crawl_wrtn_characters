import unittest
from io import BytesIO
from PIL import Image
import base64
import pymysql
import os

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = pymysql.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "root"),
            database=os.environ.get("DB_NAME", "wrtn"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.connection.close()

    def test_record_counts(self):
        self.cursor.execute("SELECT COUNT(*) FROM character_category")
        category_count = self.cursor.fetchone()['COUNT(*)']
        self.cursor.execute("SELECT COUNT(*) FROM character_info")
        info_count = self.cursor.fetchone()['COUNT(*)']
        self.assertEqual(category_count, 100, f"Category count is {category_count}, expected 100.")
        self.assertEqual(info_count, 100, f"Info count is {info_count}, expected 100.")

    def test_no_duplicates(self):
        self.cursor.execute("""
            SELECT name, description, initial_message, COUNT(*)
            FROM character_info 
            GROUP BY name, description, initial_message 
            HAVING COUNT(*) > 1
        """)
        info_duplicates = self.cursor.fetchall()
        self.assertEqual(len(info_duplicates), 0, f"Found duplicates in character_info: {info_duplicates}")

    def test_no_null_values(self):
        self.cursor.execute("SELECT COUNT(*) FROM character_category WHERE name IS NULL")
        category_null_count = self.cursor.fetchone()['COUNT(*)']
        self.cursor.execute("SELECT COUNT(*) FROM character_info WHERE name IS NULL")
        info_null_count = self.cursor.fetchone()['COUNT(*)']
        self.assertEqual(category_null_count, 0, f"Found NULL values in character_category: {category_null_count}")
        self.assertEqual(info_null_count, 0, f"Found NULL values in character_info: {info_null_count}")

    def test_random_image_check(self):
        self.cursor.execute("SELECT * FROM character_info ORDER BY rand() LIMIT 1")
        result = self.cursor.fetchone()

        image_blob = result.pop('image_blob')
        image_data = base64.b64decode(image_blob)
        image = Image.open(BytesIO(image_data))

        image.save(os.path.join(os.getcwd(), "character_img.png"))

if __name__ == "__main__":
    unittest.main()