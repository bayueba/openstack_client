import json
import requests


class GlanceClient:

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
            if endpoint['name'] == 'glance':
                self.glance_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.glance_endpoint == "":
            print "no endpoint of glance found"
            raise Exception

        self.glance_headers = {'X-Auth-Token': token_id}

    def images_list(self):

        ret = requests.get("%s/v2/images" % (self.glance_endpoint),
                           headers=self.glance_headers)
        if not ret.status_code == 200:
            print "get images list failed and staus code is %s"\
                   % ret.status_code
            raise Exception

        imgs_list = json.loads(ret.text)

        return imgs_list


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    glanceClient = GlanceClient(username,
                                password,
                                tenant_id,
                                auth_url
                                )
    imgs_list = glanceClient.images_list()

    print imgs_list

if __name__ == "__main__":
    main()
