import json
import logging
import time

import requests


class Http:

    def get_logger(self):
        return logging.getLogger(__name__)

    def get(self, url, auth):
        # self.getLogger().info('URL {}'.format(url))
        try:
            r = requests.get(url, auth= auth)
        except Exception as ex:
            self.get_logger().info(ex)
            time.sleep(1)
            return super().get(url, auth)
        return r.status_code, self.__to_object(r.text)

    def put(self, url, auth, data=None):
        self.get_logger().info('URL {}'.format(url))
        r = requests.put(url, self.__to_json(data), auth=auth)
        return (r.status_code, self.__to_object(r.text))

    def post(self, url, data, auth):
        if data is not None:
            data = self.__to_json(data)

        # self.get_logger().info('{} {}'.format( type(data), data))
        try:
            r = requests.post(url=url, json=data, auth=auth)
        except Exception as ex:
            self.get_logger().info('{} retrying in 1 second...'.format(ex))
            time.sleep(1)
            return super().post(url, data, auth)

        return r.status_code, self.__to_object(r.text)

    def __to_object(self, string):
        # self.getLogger().info('{}'.format(str))
        return json.loads(string)

    def __to_json(self, obj):

        if obj is None:
            return ''
        return json.dumps(obj)