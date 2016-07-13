import json
import requests


class CeilometerClient:

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
            if endpoint['name'] == 'ceilometer':
                self.ceilometer_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.ceilometer_endpoint == "":
            print "no endpoint of ceilometer found"
            raise Exception

        self.ceilometer_headers = {'X-Auth-Token': token_id}

    def get_resouce(self):

        ret = requests.get("%s/v2/resources" % (self.ceilometer_endpoint),
                           headers=self.ceilometer_headers)
        if not ret.status_code == 200:
            print "get volumes info failed and status code is %s"\
                    % ret.status_code
            raise Exception

        resources = json.loads(ret.text)

        return resources


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    ceilometerClient = CeilometerClient(username,
                                password,
                                tenant_id,
                                auth_url
                                )
    sources_list = ceilometerClient.get_resouce()
    print sources_list

if __name__ == "__main__":
    main()
