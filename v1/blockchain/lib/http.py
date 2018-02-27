import json

import requests

class Http:

    def get(self, url, auth):
        r = requests.get(url, auth= auth)
        return (r.status_code, self.__toObject(r.text))

    def put(self, url, auth, data=None):
        r = requests.put(url, self.__tojson(data), auth=auth)
        return (r.status_code, self.__toObject(r.text))


    def __toObject(self, str):
        return json.loads(str)

    def __tojson(self, obj):
        if obj is None:
            return ''
        return json.dumps(obj)