from datetime import datetime, timedelta
import bcrypt
from decorators import create_session_token
from dotenv import load_dotenv
import os
from .Images import Images
dotenv_path = os.path.join(os.path.abspath(os.pardir), '.env')

# Load the .env file
load_dotenv()
USER_SESSION_TOKEN_KEY = \
    "https://www.youtube.com/watch?v=L_pRTyuZ9fk+" \
    "https://www.youtube.com/watch?v=x8VYWazR5mE+" \
    "https://www.youtube.com/watch?v=agcoHM2CJ3s+" \
    "https://www.youtube.com/watch?v=vB8sxY_PJ_w+" \
    "https://www.youtube.com/watch?v=TXfJVNqaHiM"


# shinigame + yorunikakeru + parasite + yoidore shirazu + Shippai-saku shōjo

class User:
    def __init__(self, id, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @staticmethod
    def check_password(password, stored_hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

    @staticmethod
    def get_user_listings(cursor, username):
        query = "SELECT * FROM Listings WHERE belong_user = %s"
        cursor.execute(query, (username,))
        return cursor.fetchall()

    @staticmethod
    def create_session_token(id, username):
        # After successful login
        token = create_session_token(id, username)
        return token

    @staticmethod
    def create_user(cursor, username, password, email, ip, location):
        hashed_password = User.hash_password(password)
        query = "INSERT INTO Users (username, password, email, registered_at, IP, location) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
        values = (username, hashed_password, email, datetime.now(), ip, location)
        cursor.execute(query, values)
        user_id = cursor.fetchone()[0]
        os.mkdir(f"{os.getenv('ABSOLUTE_PATH')}marketplace_backend/Assets/users/{user_id}")
        os.mkdir(f"{os.getenv('ABSOLUTE_PATH')}marketplace_backend/Assets/users/{user_id}/listings")
        # replace with actual path on VPS
        return user_id

    def delete_user(self, cursor):
        query = "DELETE FROM Users WHERE id = %s or username = %s"
        value = (self.username, self.email)
        cursor.execute(query, value)

    @staticmethod
    def check_user_exist(cursor, id=None, username=None, email=None, return_result=None):
        cursor.execute("SELECT * FROM Users WHERE id = %s OR username = %s OR email = %s", (id, username, email))
        existing_users = cursor.fetchall()
        if return_result:
            for user in existing_users:
                if user[1] == username and user[3] == email:
                    return 1
                else:
                    return 3
        else:
            for user in existing_users:
                if user[1] == username:
                    return 1
                elif user[3] == email:
                    return 2
                else:
                    return 3

    @staticmethod
    def change_user_info(cursor, id, username, email):
        if username:
            update_query = """
                UPDATE Users
                SET username = %s
                WHERE id = %s
                """
            cursor.execute(update_query, (username, id))
        if email:
            update_query = """
                UPDATE Users
                SET email = %s
                WHERE id = %s
                """
            cursor.execute(update_query, (email, id))

    @staticmethod
    def check_repeat(cursor, username=None, email=None):
        username_query = "SELECT COUNT(*) FROM Users WHERE username = %s"
        email_query = "SELECT COUNT(*) FROM Users WHERE email = %s"
        cursor.execute(username_query, (username,))
        user_count = cursor.fetchone()[0]
        cursor.execute(email_query, (email,))
        email_count = cursor.fetchone()[0]
        status = 0
        if user_count > 0 and email_count > 0:
            status = 3
        elif user_count > 0:
            status = 2
        elif email_count > 0:
            status = 1
        return status

    @staticmethod
    def change_avatar(image, user_id, db):
        if image:
            file_path = f"{os.getenv('ABSOLUTE_PATH')}marketplace_backend/Assets/users/{user_id}/avatar.jpg"
            # edit path to real server path
            Images(id=user_id, db=db).avatar_image(image)
            return True
        else:
            return False

    def get_user_posts(self, cursor):
        query = "SELECT id FROM Listings WHERE belong_user = %s"
        cursor.execute(query, (self.username,))
        listing_id = cursor.fetchall()[1]
        return listing_id

    @staticmethod
    def get_user_by_username(cursor, username):
        query = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row:
            return User(row['username'], row['password_hash'])
        else:
            return None

    @staticmethod
    def get_user_by_criteria(cursor, id=None, username=None, email=None):
        cursor.execute("SELECT * FROM Users WHERE id = %s OR username = %s OR email = %s", (id, username, email))
        return cursor.fetchone()

    @staticmethod
    def get_userdata(cursor, id=None, username=None, email=None):
        cursor.execute(
            "SELECT id, username, registered_at, description FROM Users WHERE id = %s OR username = %s OR email = %s",
            (id, username, email))
        return cursor.fetchone()

    @staticmethod
    def get_user_for_login(cursor, id=None, username=None, email=None):
        cursor.execute(
            "SELECT id, username, password FROM Users WHERE id = %s OR username = %s OR email = %s",
            (id, username, email))
        result = cursor.fetchone()
        if result is not None:
            id, username, password = result
            return id, username, password
        else:
            return False


