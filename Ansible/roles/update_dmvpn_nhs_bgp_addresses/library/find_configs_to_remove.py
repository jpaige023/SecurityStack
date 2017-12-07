#!/usr/bin/env python

import re
import yaml
import io

def main():
    module = AnsibleModule(
            argument_spec=dict(
                runconfig = dict(required=True, type='str'),
                tunnel_number = dict(required=True, type='str')
                 ))
    dmvpn_number = module.params['tunnel_number']
    interface_name = "interface Tunnel" + dmvpn_number
    # Replace Single Quote in Running-config to prevent error loading as yaml
    answer = module.params['runconfig']
    answer1 = answer.replace('"', "XXXX")
    answer2 = answer1.replace("'", '"')
    yanswer = yaml.load(answer2)

    # Find DMVPN Tunnel Interface and all NHRP sub-commands in running-config
    interface_commands_dictionary = {}
    data_relevant = []
    for line in yanswer["stdout_lines"][0]:
        if line == "":
            pass
        elif line[0] != " ":
            last_parent = line
            if last_parent == interface_name:
                data_relevant.append(line)
                temp_list = []
                interface_commands_dictionary[line] = temp_list
        elif last_parent == interface_name:
            if line[0] == " ":
                temp_list.append(line)
    # Pull Ip addresses from Tunnel interface NHRP commands
    addresses_nhrp = []
    for command in temp_list:
        if re.search(r"^ ip nhrp nhs", command):
            command1 = command.lstrip(' ip nhrp nhs ')
            new_ip = ""
            for i in command1:
                if i == " ":
                    break
                else:
                    new_ip += str(i)
            addresses_nhrp.append(new_ip)

    # Collect Current NHS/BGP addresses
    with open("../DB/dmvpn_tunnel_nhs_addresses.yml", 'r') as yml_data:
        dictionary_initial_read = yaml.load(yml_data)
    list_of_tunnel_dmvpn_addresses = []
    for item in dictionary_initial_read["dmvpn_addresses"][dmvpn_number]:
        list_of_tunnel_dmvpn_addresses.append(item['dmvpn_address'])
    # If NHRP addresses are in configuration that shouldn't be there: add to remove list
    addresses_to_remove = []
    for address in addresses_nhrp:
        if address not in list_of_tunnel_dmvpn_addresses:
            addresses_to_remove.append(address)

    module.exit_json(changed=False, addresses_to_remove=addresses_to_remove)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

main()
