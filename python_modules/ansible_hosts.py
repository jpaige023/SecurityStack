import simplejson as json

def main(cloud_provider, region, vpc_template, vpc_number, dictionary_tfvars):
#def main():
    # cloud_provider = "aws"
    # region = "us-west-2"
    # vpc_template = "high_availability"
    # vpc_number = "12"

    tfstate_dictionary = {"ip_a": None, "ip_b": None, "route_table_var": None, "eni_a_var": None, "eni_b_var": None}

    if cloud_provider == "aws":
        with open("VPCs/{}/terraform.tfstate".format(vpc_number)) as json_data:
            d = json.load(json_data)
            tfstate_dictionary["ip_a"] = d["modules"][0]["resources"]["aws_eip.CSR1000vA"]["primary"]["attributes"]["public_ip"]
            if vpc_template == "high_availability":
                tfstate_dictionary["ip_b"] = d["modules"][0]["resources"]["aws_eip.CSR1000vB"]["primary"]["attributes"]["public_ip"]
                tfstate_dictionary["route_table_var"] = d["modules"][0]["resources"]["aws_route_table.{}-private".format(region)]["primary"]["id"]
                tfstate_dictionary["eni_a_var"] = d["modules"][0]["resources"]["aws_network_interface.G2A"]["primary"]["id"]
                tfstate_dictionary["eni_b_var"] = d["modules"][0]["resources"]["aws_network_interface.G2B"]["primary"]["id"]

    if cloud_provider == "azure":
        with open("VPCs/{}/terraform.tfstate".format(vpc_number)) as json_data:
            d = json.load(json_data)
            tfstate_dictionary["ip_a"] = d["modules"][0]["resources"]["azurerm_public_ip.PIP1"]["primary"]["attributes"]["ip_address"]
            if vpc_template == "high_availability":
                tfstate_dictionary["ip_b"] = d["modules"][0]["resources"]["azurerm_public_ip.PIP2"]["primary"]["attributes"]["ip_address"]

    tfstate_dictionary.update(dictionary_tfvars)

    with open('Ansible/host_vars/{}.json'.format(tfstate_dictionary["ip_a"]), 'w') as outfile:
        json.dump(tfstate_dictionary, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    if tfstate_dictionary["ip_b"]:
        with open('Ansible/host_vars/{}.json'.format(tfstate_dictionary["ip_b"]), 'w') as outfile:
            json.dump(tfstate_dictionary, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)


if __name__ == "__main__":
   main()