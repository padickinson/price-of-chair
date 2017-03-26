import uuid
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors
from src.common.database import Database


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "name":self.name,
            "url_prefix":self.url_prefix,
            "tag_name":self.tag_name,
            "query":self.query,
            "_id":self._id
        }

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json())
        #Database.insert(StoreConstants.COLLECTION, self.json())

    @classmethod
    def get_by_id(cls,id):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{"_id":id}))


    @classmethod
    def get_by_name(cls,name):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{"name":name}))

    @classmethod
    def get_store_list(cls):
        return [cls(**store) for store in Database.find(StoreConstants.COLLECTION,{})]

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        try:
            result = Database.find_one(
                StoreConstants.COLLECTION, {"url_prefix": {"$regex":'^{}'.format(url_prefix)}})
            store = cls(**result)
            if store is not None:
                return store
        except Exception as e:
            return None

    @classmethod
    def find_by_url(cls,url):
        """
        return a store from a URL like https://www.amazon.com/Amazon-Echo-Bluetooth-Speaker-with-WiFi-Alexa/dp/B00X4WHP5E
        :param url:
        :return: matvhing store, or raises StoreNotFoundError if no store.
        """
        for i in range(len(url)+1):
            store = cls.get_by_url_prefix(url[:len(url)-i])
            if store is not None:
                return store

        raise StoreErrors.StoreNotFoundError("No store found for url {}".format(url))

    def delete(self):
        Database.delete_one(StoreConstants.COLLECTION,{"_id":self._id})