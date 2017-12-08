import yaml
import io

def main(tfstate_dictionary):
# def main():
#     tfstate_dictionary = {"dmvpn_tunnel": "1", "ip_a": "1.1.1.31", "router_a_address_g1": "10.1.1.31", "tunnel_address": "10.254.10.10"}

    # Add hub ip addresses to dmvpn_tunnel_nhs_addresses
    with open("DB/dmvpn_per_ mgre_nhs_bgp_rr_address_info.yml", 'r') as yml_data:
        dictionary_initial_read = yaml.load(yml_data)

    dictionary_nhs_full = {}
    # If hub tunnel x is already in there, add the addresses for the new hub site
    if tfstate_dictionary["dmvpn_tunnel"] in dictionary_initial_read["dmvpn_addresses"]:
        nhs_updates = {'dmvpn_address': tfstate_dictionary["tunnel_address"], 'public': tfstate_dictionary["ip_a"],
                        'private': tfstate_dictionary["router_a_address_g1"]}
        dictionary_nhs_full.update(dictionary_initial_read)
        dictionary_nhs_full["dmvpn_addresses"][tfstate_dictionary["dmvpn_tunnel"]].append(nhs_updates)
    # If hub tunnel x is not there, add tunnel x plus the addresses
    else:
        nhs_updates = [{'dmvpn_address': tfstate_dictionary["tunnel_address"], 'public': tfstate_dictionary["ip_a"],
                        'private': tfstate_dictionary["router_a_address_g1"]}]
        dictionary_nhs_full.update(dictionary_initial_read)
        dictionary_nhs_full["dmvpn_addresses"][tfstate_dictionary["dmvpn_tunnel"]] = nhs_updates

    # Write the new dmvpn_tunnel_nhs_addresses file
    with io.open('DB/dmvpn_per_ mgre_nhs_bgp_rr_address_info.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(dictionary_nhs_full, outfile, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
   main()