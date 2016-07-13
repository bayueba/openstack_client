import json
import requests


class IronicClient:

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
            if endpoint['name'] == 'ironic':
                self.ironic_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.ironic_endpoint == "":
            print "no endpoint of ironic found"
            raise Exception

        self.ironic_headers = {'X-Auth-Token': token_id}

    def nodes_list(self):

        ret = requests.get("%s/v1/nodes/detail" % self.ironic_endpoint,
                           headers=self.ironic_headers)
        if not ret.status_code == 200:
            print "get node list failed and status code is %s"\
                   % ret.status_code
            raise Exception

        nodes_list = json.loads(ret.text)

        return nodes_list


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    ironicClient = IronicClient(username,
                                password,
                                tenant_id,
                                auth_url
                                )
    node_props = ironicClient.nodes_list()
    print node_props

if __name__ == "__main__":
    main()
