import json
import logging
import time

import requests


class Http:

    def get_logger(self):
        return logging.getLogger(__name__)

    def callget(self, url, auth):
        try:
            r = requests.get(url, auth= auth)
        except Exception as ex:
            self.get_logger().info("Error {}".format(ex))
            return None, None

        return r.status_code, self.__to_object(r.text)

    def callput(self, url, auth, data=None):
        self.get_logger().info('URL {}'.format(url))
        r = requests.put(url, self.__to_json(data), auth=auth)
        return (r.status_code, self.__to_object(r.text))

    def callpost(self, url, data, auth, retry=1):
        if data is not None:
            data = self.__to_json(data)
        try:
            r = requests.post(url=url, data=data, auth=auth, headers=self.get_headers())
        except Exception as ex:
            self.get_logger().info('Error {}'.format(ex))
            return None, None
        return r.status_code, self.__to_object(r.text)

    def get_headers(self):
        return {'Content-type': 'application/json'}

    def __to_object(self, string):
        return json.loads(string)

    def __to_json(self, obj):
        if obj is None:
            return None
        if isinstance(obj, str):
            return obj;
        return json.dumps(obj)