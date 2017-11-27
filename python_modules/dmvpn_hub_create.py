import simplejson as json

def main(tfstate_dictionary):
# def main():
#     tfstate_dictionary = {"dmvpn_tunnel": "1", "ip_a": "1.1.1.31", "router_a_address_g1": "10.1.1.31"}

    # Add hub ip address to hub list
    with open('DB/dmvpn_tunnel_nhs_addresses.json') as json_data:
        dictionary_initial_read = json.load(json_data)
    dictionary_nhs_full = {}
    if tfstate_dictionary["dmvpn_tunnel"] in dictionary_initial_read:
        dictionary_nhs_addresses_initial = dictionary_initial_read[tfstate_dictionary["dmvpn_tunnel"]]
        dictionary_nhs_addresses_updated = dictionary_initial_read[tfstate_dictionary["dmvpn_tunnel"]]
        dictionary_nhs_addresses_updated[tfstate_dictionary["router_a_address_g1"]] = tfstate_dictionary["ip_a"]
        dictionary_nhs_full.update(dictionary_initial_read)
        dictionary_nhs_full[tfstate_dictionary["dmvpn_tunnel"]].update(dictionary_nhs_addresses_updated)
    else:
        dictionary_nhs_full[tfstate_dictionary["dmvpn_tunnel"]] = {
            tfstate_dictionary["router_a_address_g1"]: tfstate_dictionary["ip_a"]}

    with open('DB/dmvpn_tunnel_nhs_addresses.json', 'w') as new_json_data:
        json.dump(dictionary_nhs_full, new_json_data, sort_keys=True, indent=4,
                  ensure_ascii=False)


if __name__ == "__main__":
   main()