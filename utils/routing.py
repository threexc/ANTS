#!/usr/bin/python3

import os
import subprocess

class ANTS_Route():

    def __init__(self, server_ip, client_ip):

        # Set a default server ip if none is given
        if server_ip == None:
            self.server_ip = "10.1.1.120"
        else:
            self.server_ip = server_ip

        # Set a default client ip if none is given
        if client_ip = None:
            self.client_ip = "10.1.11.115"
        else:
            self.client_ip = client_ip

        self.server_device_name = None
        self.server_device_mac = None
        self.client_device_name = None
        self.client_device_mac = None

        self.device_list = os.listdir("/sys/class/net")
        self.device_list.remove("lo")

    def flush_routing(self):
        self.flush_args = "iptables -t nat -F".split(" ")
        self.flush_proc = subprocess.call(self.flush_args)

        while True:
            self.flush_proc.poll()
            if self.flush_proc.returncode is not None:
                break

        print("iptables settings now cleared.")

    def get_mac_addrs(self, server_device, client_device):
        if server_device = None:
            self.server_device_name = self.device_list[2]
        else:
            self.server_device_name = server_device
        if client_devce = None:
            self.client_device_name = self.device_list[0]
        else:
            self.client_device_name = client_device
            
        print("{0} and {1} will now be configured for routing.\n".format(self.server_device_name, self.client_device_name))
        with open("/sys/class/net/{0}/address".format(self.server_device_name)) as f:
            self.server_device_mac = f.readline().rstrip("\n")
        with open("/sys/class/net/{0}/address".format(self.client_device_name)) as f:
            self.client_device_mac = f.readline().rstrip("\n")

        print("Server device MAC address is {0}\n".format(self.server_device_mac))
        print("Client device MAC address is {0}\n".format(self.client_device_mac))


    def configure_device_ips(self):
        print("Setting up IP addresses...\n")

        self.server_ip_args = "ip addr add {0}/24 dev {1}".format(self.server_ip, self.server_device_name).split(" ")
        self.client_ip_args = "ip addr add {0}/24 dev {1}".format(self.client_ip, self.client_device_name).split(" ")

        subprocess.call(self.server_ip_args)
        subprocess.call(self.client_ip_args)

    def configure_iptables_rules(self):
        print("Configuring iptables...\n")

        self.iptables_postrouting_one = "iptables -t nat -A POSTROUTING -s {0} -d 10.2.11.115 -j SNAT --to-source 10.2.1.120".format(self.server_ip).split(" ")
        self.iptables_prerouting_one = "iptables -t nat -A PREROUTING -d 10.2.1.120 -j DNAT --to-destination {0}".format(self.server_ip).split(" ")
        self.iptables_postrouting_two = "iptables -t nat -A POSTROUTING -s {0} -d 10.2.1.120 -j SNAT --to-source 10.2.11.115".format(self.client_ip).split(" ")
        self.iptables_prerouting_two = "iptables -t nat -A PREROUTING -d 10.2.11.115 -j DNAT --to-destination {0}".format(self.client_ip).split(" ")

        subprocess.call(self.iptables_postrouting_one)
        subprocess.call(self.iptables_prerouting_one)
        subprocess.call(self.iptables_postrouting_two)
        subprocess.call(self.iptables_prerouting_two)

    def list_iptables_config(self):
        print("iptables configuration status:\n")

        self.iptables_list_args = "iptables -t nat -L".split(" ")
        subprocess.call(self.iptables_list_args)

    def add_routes(self):
        print("Adding routes for {0} ({1}) and {2} ({3})\n".format(self.server_device_name, self.server_device_mac, self.client_device_name, self.client_device_mac))

        self.ip_route_one_args = "ip route add 10.2.11.115 dev {0}".format(self.server_device_name).split(" ")
        self.arp_one_args = "arp -i {0} -s 10.2.11.115 {1}".format(self.server_device_name, self.client_device_mac).split(" ")

        self.ip_route_two_args = "ip route add 10.2.1.120 dev {0}".format(self.client_device_name).split(" ")
        self.arp_two_args = "arp -i {0} -s 10.2.1.120 {1}".format(self.client_device_name, self.server_device_mac).split(" ")

        subprocess.call(self.ip_route_one_args)
        subprocess.call(self.arp_one_args)
        subprocess.call(self.ip_route_two_args)
        subprocess.call(self.arp_two_args)
