import requests
from common.project_path import *


class HttpRequest:
    def __init__(self, url, param):
        self.url = url
        self.param = param

    def http_request(self, method, payload=None, token=None):
        headers = {'token': token}
        if payload == 'json':
            headers['Content-Type'] = 'application/json'
            if method.upper() == 'GET':
                result = requests.get(self.url, json=self.param, headers=headers)
            elif method.upper() == 'POST' and 'filename' not in self.param.keys():
                result = requests.post(self.url, json=self.param, headers=headers)

        elif method.upper() == 'GET':
            result = requests.get(self.url, params=self.param, headers=headers)
        elif method.upper() == 'POST' and 'filename' not in self.param.keys():
            result = requests.post(self.url, data=self.param, headers=headers, verify=False)

        elif method.upper() == 'POST' and 'filename' in self.param.keys():
            list_1 = []
            file_param = self.param['filename'][0]
            for index, img in enumerate(self.param['filename']):
                if index != 0:
                    tuples = (file_param, open(os.path.join(picture_path, img), 'rb'))
                    list_1.append(tuples)
            self.param.pop('filename')
            result = requests.post(self.url, headers=headers, data=self.param, files=list_1)
        else:
            result = requests.post(self.url, data=self.param, headers=headers)
        return result

if __name__ == '__main__':
    pass
    # pp =  [('file',open('filename','rb'),'image/jpg'),('file',open('filename','rb'),'image/jpg')]