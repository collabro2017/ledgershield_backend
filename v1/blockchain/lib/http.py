import json
import logging
import time

import requests


class Http:

    def get_logger(self):
        return logging.getLogger(__name__)

    def callget(self, url, auth):
        # self.getLogger().info('URL {}'.format(url))
        try:
            r = requests.get(url, auth= auth)
        except Exception as ex:
            self.get_logger().info(ex)
            time.sleep(1)
            return self.callget(url, auth)
        return r.status_code, self.__to_object(r.text)

    def callput(self, url, auth, data=None):
        self.get_logger().info('URL {}'.format(url))
        r = requests.put(url, self.__to_json(data), auth=auth)
        return (r.status_code, self.__to_object(r.text))

    def callpost(self, url, data, auth):
        if data is not None:
            data = self.__to_json(data)

        self.get_logger().info('{}'.format(url))
        self.get_logger().info('{} {}'.format( type(data), data))
        try:

            r = requests.post(url=url, data=data, auth=auth, headers=self.get_headers())
        except Exception as ex:
            self.get_logger().info('{} retrying in 1 second...'.format(ex))
            time.sleep(1)
            return self.callpost(url, data, auth)
        self.get_logger().info('{} {}'.format(r.status_code, r.text))
        return r.status_code, self.__to_object(r.text)

    def get_headers(self):
        return {'Content-type': 'application/json'}
    def __to_object(self, string):
        # self.getLogger().info('{}'.format(str))
        return json.loads(string)

    def __to_json(self, obj):

        if obj is None:
            return None
        return json.dumps(obj)