import datetime
import uuid
import requests
import src.models.alerts.constants as AlertConstants
from src import config
from src.common.database import Database
from src.models.items.item import Item
from dateutil import tz



class Alert(object):
    def __init__(self, user_id, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_id = user_id
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.active = active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on {} with price {}>".format(
            self.get_user_email(), self.item.name, self.price_limit
        )

    def get_user_email(self):
        from src.models.users.user import User
        return User.get_by_id(self.user_id).email

    def get_last_checked_local(self):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        utc = self.last_checked

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        local_time = utc.astimezone(to_zone)

        return local_time

    def json(self):
        return {
            "user_id": self.user_id,
            "price_limit": self.price_limit,
            "item_id": self.item._id,
            "last_checked": self.last_checked,
            "active": self.active,
            "_id": self._id
        }

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.get_user_email(),
                "subject": "Price limit reached for {} ".format(self.item.name),
                "text": "We found a deal on {} ({}). To see the alert, visit {}".format(
                    self.item.name, self.item.url, "{}/alerts/{}".format(config.server, self._id))
            }
        )

    def do_price_check(self):
        self.item.load_price()
        self.item.save_to_mongo()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price <= self.price_limit:
            self.send()

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(
            AlertConstants.COLLECTION, {"last_checked": {"$lte": last_updated_limit},
                                        "active": True}
        )]

    @classmethod
    def get_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))

    @classmethod
    def get_by_user_id(cls, user_id):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_id": user_id})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete_from_db(self):
        Database.delete_one(AlertConstants.COLLECTION,{"_id": self._id})