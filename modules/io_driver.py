from Adafruit_IO import Client, Feed, RequestError, Data
import config


class IODriver:
    def write_to(data):
        pass

    def read_from():
        pass


FILE_NAME = "output.txt"

class FileDriver(IODriver):
    def __init__(self):
        self.file_name = FILE_NAME

    def read_from(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
        return data

    def write_to(self, data):
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(data)
            f.close()


ADAFRUIT_IO_FEED_NAME = "DefaceCheckStaticHashes"
ADAFRUIT_IO_FEED_KEY = "defacecheckstatichashes"


class AdafruitIODriver(IODriver):
    def __init__(self):
        self.client = Client(config.ADAFRUIT_IO_USERNAME,
                             config.ADAFRUIT_IO_KEY)
        self.feed = self.get_default_feed()

    def get_default_feed(self):
        try:
            feed = self.client.feeds(ADAFRUIT_IO_FEED_KEY)
        except RequestError:
            feed = Feed(name=ADAFRUIT_IO_FEED_NAME, key=ADAFRUIT_IO_FEED_KEY, history=False)
            feed = self.client.create_feed(feed)
        return feed

    def read_from(self):
        response: Data = self.client.receive(self.feed.key)
        return response.value

    def write_to(self, data):
        self.client.send_data(self.feed.key, data)
