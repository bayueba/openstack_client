import json
import requests


class NovaClient:

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
            if endpoint['name'] == 'nova':
                self.nova_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.nova_endpoint == "":
            print "no endpoint of nova found"
            raise Exception

        self.nova_headers = {'X-Auth-Token': token_id}

    def instance_list(self):

        ret = requests.get("%s/servers/detail" % (self.nova_endpoint),
                           headers=self.nova_headers)
        if not ret.status_code == 200:
            print "get node list failed and staus code is %s"\
                   % ret.status_code
            raise Exception

        servers = json.loads(ret.text)

        return servers

    def flavors_list(self):

        ret = requests.get("%s/flavors" % (self.nova_endpoint),
                           headers=self.nova_headers)
        if not ret.status_code == 200:
            print "get flavors info failed and status code is %s"\
                    % ret.status_code
            raise Exception

        flaovrs = json.loads(ret.text)

        return flavors


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    novaClient = NovaClient(username,
                            password,
                            tenant_id,
                            auth_url
                            )
    nodes_list = novaClient.instance_list()
    print nodes_list

if __name__ == "__main__":
    main()
