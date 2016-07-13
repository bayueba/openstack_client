import json
import requests


class MagnumClient:

    def __init__(self, username, password, tenant_id, auth_url):

        data = {"auth": {}}
        data["auth"]["passwordCredentials"] = {
            "username": username,
            "password": password
        }
        data["auth"]["tenantId"] = tenant_id
        data = json.dumps(data)

        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }

        ret = requests.post(auth_url, data=data, headers=headers)
        if not ret.status_code == 200:
            raise Exception

        token_id = ret.json()['access']['token']['id']

        for endpoint in ret.json()['access']['serviceCatalog']:
            if endpoint['name'] == 'magnum':
                self.magnum_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.magnum_endpoint == "":
            print "no endpoint of nova found"
            raise Exception

        self.magnum_headers = {'X-Auth-Token': token_id}

    def baymodel_list(self):

        ret = requests.get("%s/baymodels" % (self.magnum_endpoint),
                           headers=self.magnum_headers)

        if not ret.status_code == 200:
            print "get baymodels list failed and status code is %s"\
                   % ret.status_code
            raise Exception

        model_list = json.loads(ret.text)

        return model_list

    def bay_list(self):

        ret = requests.get("%s/bays" % (self.magnum_endpoint),
                           headers=self.magnum_headers)

        if not ret.status_code == 200:
            print "get bays list failed and status code is %s"\
                   % ret.status_code
            raise Exception

        bay_list = json.loads(ret.text)

        return bay_list

    def pod_list(self):

        ret = requests.get("%s/pods" % (self.magnum_endpoint),
                           headers=self.magnum_headers)

        if not ret.status_code == 200:
            print "get pods list failed and status code is %s"\
                   % ret.status_code
            raise Exception

        pod_list = json.loads(ret.text)

        return pod_list


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    magnumClient = MagnumClient(username,
                                password,
                                tenant_id,
                                auth_url
                                )
    model_list = magnumClient.pod_list()
    print model_list

if __name__ == "__main__":
    main()
