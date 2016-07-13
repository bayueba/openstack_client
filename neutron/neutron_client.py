import json
import requests


class NeutronClient:

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
            if endpoint['name'] == 'neutron':
                self.neutron_endpoint = endpoint['endpoints'][0]['publicURL']
                break
        if self.neutron_endpoint == "":
            print " no endpoint of neutron found"
            raise Exception

        self.neutron_headers = {'X-Auth-Token': token_id}

    def net_list(self):

        ret = requests.get("%s/v2.0/networks" % (self.neutron_endpoint),
                           headers=self.neutron_headers)
        if not ret.status_code == 200:
            print "get net list failed and staus code is %s" % ret.status_code
            raise Exception

        networks = json.loads(ret.text)

        return networks

    def subnet_list(self):

        ret = requests.get("%s/v2.0/subnets" % (self.neutron_endpoint),
                           headers=self.neutron_headers)
        if not ret.status_code == 200:
            print "get subnets list failed and staus code is %s"\
                   % ret.status_code
            raise Exception

        subnets = json.loads(ret.text)

        return subnets

    def port_list(self):

        ret = requests.get("%s/v2.0/ports" % (self.neutron_endpoint),
                           headers=self.neutron_headers)
        if not ret.status_code == 200:
            print "get ports list failed and staus code is %s"\
                   % ret.status_code
            raise Exception

        ports = json.loads(ret.text)

        return ports


def main():
    username = "admin"
    password = "password"
    tenant_id = "fc9cbbb0767543e889f6c688d2452c42"
    auth_url = 'http://10.101.58.6:5000/v2.0/tokens'

    neutronClient = NeutronClient(username,
                                  password,
                                  tenant_id,
                                  auth_url
                                  )
    port_list = neutronClient.port_list()
    print port_list

if __name__ == "__main__":
    main()
