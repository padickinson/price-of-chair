import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price =None, _id = None):
        self.name = name
        self.url = url
        self.store = Store.find_by_url(url)
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # Amazon: <span id-"priceblock_ourprice" class="
        # for amazon store, tag_name = span, and query = {"id":"priceblock_ourprice"}
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.store.tag_name, self.store.query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)") # need brackets for matching group
        match = pattern.search(string_price)
        self.price =  float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id':self._id}, self.json())


    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_by_url(cls,url):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"url": url}))

    def json(self):
        return{
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "_id": self._id
        }