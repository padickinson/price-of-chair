import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email,password combo as sent by site forms is valid or not
        Checks that the email exists, and that the password associated with the email is correct
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION,{"email":email}) # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
            pass
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
            pass

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using email and password.
        The password comes hashed as sha-512
        :param email: email, might be invalid
        :param password: sha512 hashed password
        :return: True if registered successfully, or false otherwise (exceptions may be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("A user with email {} already exists.".format(email))

        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("{} is not a valid email address".format(email))
        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def get_alerts(self):
        return Alert.get_by_user_id(self._id)

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_by_name(cls, name):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"name": name}))

    @classmethod
    def get_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))