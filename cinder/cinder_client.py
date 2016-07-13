import json
import requests


class CinderClient:

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
            if endpoint['name'] == 'cinder':
                self.cinder_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.cinder_endpoint == "":
            print "no endpoint of cinder found"
            raise Exception

        self.cinder_headers = {'X-Auth-Token': token_id}

    def volume_list(self):

        ret = requests.get("%s/volumes" % (self.cinder_endpoint),
                           headers=self.cinder_headers)
        if not ret.status_code == 200:
            print "get volumes info failed and status code is %s"\
                    % ret.status_code
            raise Exception

        volumes = json.loads(ret.text)

        return volumes

    def volume_detail(self):

        ret = requests.get("%s/volumes/detail" % (self.cinder_endpoint),
                           headers=self.cinder_headers)
        if not ret.status_code == 200:
            print "get volumes details info failed and status code is %s"\
                    % ret.status_code
            raise Exception

        volume_detail = json.loads(ret.text)

        return volume_detail


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    cinderClient = CinderClient(username,
                                password,
                                tenant_id,
                                auth_url
                                )
    volume_list = cinderClient.volume_detail()
    print volume_list

if __name__ == "__main__":
    main()
