import uuid
import os


class Images:
    def __init__(self, db, id, username=None):
        self.username = username
        self.id = id
        self.db = db

    def save_image(self, imag_path):
        cursor = self.db.cursor()
        check = "SELECT * FROM Image_token WHERE system_path = %s"
        cursor.execute(check, (imag_path,))
        if cursor.fetchone() is None:
            query = "INSERT INTO Image_token (token, system_path) VALUES (%s, %s)"
            cursor.execute(query, (str(uuid.uuid4()), imag_path))
            self.db.commit()
            cursor.close()

    def listing_image(self, image_file):
        if image_file:
            file_path = f"{self.username}/listings/{self.id}/{image_file.filename}"
            self.save_image(file_path)
            image_file.save(file_path)

    def avatar_image(self, image_file):
        if image_file:
            file_path = f"{self.id}/avatar.jpg"
            absolute = f"{os.getenv('ABSOLUTE_PATH')}marketplace_backend/Assets/users/"
            self.save_image(file_path)
            image_file.save(absolute+file_path)

    @staticmethod
    def token_by_path(cursor, path):
        if os.path.isfile(f"{os.getenv('ABSOLUTE_PATH')}marketplace_backend/Assets/users/" + path):
            query = "SELECT token FROM Image_token WHERE system_path = %s"
            cursor.execute(query, (path,))
            return cursor.fetchone()[0]
        else:
            return "default-avatar"
