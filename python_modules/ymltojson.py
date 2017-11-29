import simplejson as json
import os
import yaml
import io

# with open("dmvpn_tunnel_nhs_addresses.json") as settings_json_data:
#     settings_dictionary = json.load(settings_json_data)
# print(settings_dictionary)

my_dict = {'dmvpn_addresses': [{'public': '100.100.100.100', 'private': '192.168.1.1', 'dmvpn_address': '10.254.1.1'}, {'public': '200.200.200.200', 'private': '192.168.3.3', 'dmvpn_address': '10.254.3.3'}]}

with io.open('dmvpn_tunnel_nhs_addresses4.yml', 'w', encoding='utf8') as outfile:
    yaml.dump(my_dict, outfile, default_flow_style=False, allow_unicode=True)