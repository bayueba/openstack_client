import json
import requests


class OpenstackClient:

    def __init__(self, username, password, tenant_id, auth_url, service):

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

        while True:
            # Generate nova endpoint.
            if service == 'nova':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'nova':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        print self.srv_endpoint
                        break
                if self.srv_endpoint == "":
                    print "no endpoint of Nova found"
                    raise Exception
                break

            # Generate ironic endpoint.
            elif service == 'ironic':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'ironic':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        break
                if self.srv_endpoint == "":
                    print "no endpoint of Ironic found"
                    raise Exception
                break

            # Generate glance endpoint.
            elif service == 'glance':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'glance':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        break
                if self.srv_endpoint == "":
                    print "no endpoint of Glance found"
                    raise Exception
                break

            # Generate Neutron endponit.
            elif service == 'neutron':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'neutron':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        print self.srv_endpoint
                        break
                if self.srv_endpoint == "":
                    print " no endpoint of Neutron found"
                    raise Exception
                break

            # Generate Magnum endpoint.
            elif service == 'magnum':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'magnum':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        break
                if self.srv_endpoint == "":
                    print "no endpoint of Magnum found"
                    raise Exception
                break

            # Generate Cinder endpoint
            elif service == 'cinder':
                for endpoint in ret.json()['access']['serviceCatalog']:
                    if endpoint['name'] == 'cinder':
                        self.srv_endpoint =\
                             endpoint['endpoints'][0]['publicURL']
                        break
                if self.srv_endpoint == "":
                    print "no endpoint of Magnum found"
                    raise Exception
                break

            # Exit loop
            else:
                break

        self.client_headers = {'X-Auth-Token': token_id}

    def instance_list(self):
        ret = requests.get("%s/servers/detail" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get node list failed and staus code is %s" % ret.status_code
            raise Exception
        servers = json.loads(ret.text)
        return servers

    def flavor_list(self):
        ret = requests.get("%s/flavors" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get flavors info failed and status code is %s"\
                   % ret.status_code
            raise Exception
        flavors = json.loads(ret.text)
        return flavors

    def node_list(self):
        ret = requests.get("%s/v1/nodes/detail" % self.srv_endpoint,
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get nodes list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        nodes = json.loads(ret.text)
        return nodes

    def node_port_list(self):
        ret = requests.get("%s/v1/ports" % self.srv_endpoint,
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get ports list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        port_list = json.loads(ret.text)
        return port_list

    def image_list(self):
        ret = requests.get("%s/v2/images" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get images list failed and staus code is %s"\
                   % ret.status_code
            raise Exception
        imgs_list = json.loads(ret.text)
        return imgs_list

    def net_list(self):
        ret = requests.get("%s/v2.0/networks" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get net list failed and staus code is %s" % ret.status_code
            raise Exception
        networks = json.loads(ret.text)
        return networks

    def subnet_list(self):
        ret = requests.get("%s/v2.0/subnets" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get subnets list failed and staus code is %s"\
                   % ret.status_code
            raise Exception
        subnets = json.loads(ret.text)
        return subnets

    def net_port_list(self):
        ret = requests.get("%s/v2.0/ports" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get ports list failed and staus code is %s"\
                   % ret.status_code
            raise Exception
        ports = json.loads(ret.text)
        return ports

    def baymodel_list(self):
        ret = requests.get("%s/baymodels" % (self.srv_endpoint),
                           headers=self.client_headers)

        if not ret.status_code == 200:
            print "get baymodels list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        model_list = json.loads(ret.text)
        return model_list

    def bay_list(self):
        ret = requests.get("%s/bays" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get bays list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        bay_list = json.loads(ret.text)
        return bay_list

    def pod_list(self):
        ret = requests.get("%s/pods" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get pods list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        pod_list = json.loads(ret.text)
        return pod_list

    def volume_list(self):
        ret = requests.get("%s/volumes" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get volumes list failed and status code is %s"\
                   % ret.status_code
            raise Exception
        volumes = json.loads(ret.text)
        return volumes

    def backup_list(self):
        ret = requests.get("%s/backups" % (self.srv_endpoint),
                           headers=self.client_headers)
        if not ret.status_code == 200:
            print "get volumes detail failed and status code is %s"\
                   % ret.status_code
            raise Exception
        backups = json.loads(ret.text)
        return backups


def main():
    username = "admin"
    password = "password"
    tenant_id = "602ced91cf2c4cd59d86d7bce8b53bdc"
    auth_url = 'http://10.104.0.22:5000/v2.0/tokens'

    while True:
        print "Service: nova / ironic / neutron / glance / magnum / cinder"
        service = raw_input("Enter your choice: ")
        if service not in ['nova', 'ironic', 'neutron', 'glance', 'magnum',
                           'cinder']:
            print "Please enter a currect service."
        else:
            break

    while True:
        if service == 'nova':
            print "Action: instance_list / flavor_list"
            action = raw_input("Enter your choice: ")
            if action not in ['instance_list', 'flavor_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break
        elif service == 'ironic':
            print "Action: node_list / node_port_list"
            action = raw_input("Enter your choice: ")
            if action not in ['node_list', 'node_port_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break
        elif service == 'neutron':
            print "Action: net_list / subnet_list / net_port_list"
            action = raw_input("Enter choice: ")
            if action not in ['net_list', 'subnet_list', 'net_port_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break
        elif service == 'glance':
            print "Action: image_list"
            action = raw_input("Enter your choice: ")
            if action not in ['image_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break
        elif service == 'magnum':
            print "Action: baymodel_list / bay_list / pod_list"
            action = raw_input("Enter your choice: ")
            if action not in ['baymodel_list', 'bay_list', 'pod_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break
        elif service == 'cinder':
            print "Action: volume_list / backup_list"
            action = raw_input("Enter your choice: ")
            if action not in ['volume_list', 'backup_list']:
                print "Please enter a currect action."
            else:
                method = eval('action')
                break

    Client = OpenstackClient(username,
                             password,
                             tenant_id,
                             auth_url,
                             service
                             )
    res = getattr(Client, method)
    print res()

if __name__ == "__main__":
    main()
