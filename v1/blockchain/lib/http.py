import json
import logging

import requests

class Http:
    def getLogger(self):
        return logging.getLogger(__name__)

    def get(self, url, auth):
        self.getLogger().info('URL {}'.format(url))
        r = requests.get(url, auth= auth)
        return (r.status_code, self.__toObject(r.text))

    def put(self, url, auth, data=None):
        r = requests.put(url, self.__tojson(data), auth=auth)
        return (r.status_code, self.__toObject(r.text))

    def post(self, url, data, auth):
        d =  self.__tojson(data)
        r = requests.post(url, d, auth=auth)
        return (r.status_code, self.__toObject(r.text))

    def __toObject(self, str):
        self.getLogger().info('{}'.format(str))
        return json.loads(str)

    def __tojson(self, obj):
        if obj is None:
            return ''
        return json.dumps(obj)