import requests


class APIException(Exception):
    def __init__(self, status_code, data_a):

        self.status_code = status_code
        if data_a:
            self.code = data_a['status']
            self.msg = data_a['data']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        super().__init__(message)


async def base_get(url, params):
    r = requests.get(url + params)
    if r.status_code == 200:
        data = r.json()
    else:
        raise APIException(status_code=r.status_code, data_a=r.json())

    return data
