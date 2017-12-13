import simplejson as json
import os
import subprocess
import io
import yaml



def main():
    # For Pycharm change PATH to find Terraform
    path_var = os.environ["PATH"]
    path_var_plus = path_var + ":" + "/home/vagrant"
    os.environ["PATH"] = path_var_plus

    # Which VPC to remove?
    vpc_number = vpc_number_get()

    # What routers are in this VPC?
    router_eips = router_eips_get(vpc_number)
    print(router_eips)

    # iterate through router_EIPs list for ansible to de-register routers from smartlicensing
    for eip in router_eips:
        w = subprocess.Popen(['ansible-playbook', 'cisco_smart_license_remove.yml', '--extra-vars', 'target={}'.format(eip), '-vvvv'], cwd="Ansible")
        w.wait()

    # Remove EIPs from the host lists
    f = open("Ansible/hosts")
    full_hosts = f.readlines()
    f.close()
    f = open("Ansible/hosts", "w")
    for line in full_hosts:
        line_minus_new_line = line.rstrip("\n")
        if line_minus_new_line in router_eips:
            continue
        else:
            f.write(line)
    f.close()

    # Get router or routers dmvpn addresses
    dmvpn_list_to_remove_from_ipam = []
    with open('VPCs/{}/dmvpn_ip_addresses.auto.tfvars.json'.format(vpc_number)) as json_data:
        dictionary_tfvars = json.load(json_data)
    vpc_template = dictionary_tfvars['vpc_template']
    dmvpn_role = dictionary_tfvars['dmvpn_role']
    tunnel_address = dictionary_tfvars['tunnel_address']
    dmvpn_tunnel = dictionary_tfvars['dmvpn_tunnel']
    dmvpn_list_to_remove_from_ipam.append(tunnel_address)
    if vpc_template == "high_availability":
        tunnel_b_address = dictionary_tfvars['tunnel_b_address']
        dmvpn_list_to_remove_from_ipam.append(tunnel_b_address)

    # Release DMVPN Tunnel addreses from DB ipam file
    # Load the ipam list
    # dmvpn_list_to_remove_from_ipam = ["10.255.0.3", "10.255.0.4"]
    # dmvpn_tunnel = "1"
    # import simplejson as json
    with open('DB/dmvpn_mgre_ipam.json') as json_data:
        dictionary_used_ip = json.load(json_data)
    addresses_used_list = dictionary_used_ip[dmvpn_tunnel]
    # Remove stale IPs from IPAM
    reduced_addresses_list = []
    for item in addresses_used_list:
        for key in item:
            if key not in dmvpn_list_to_remove_from_ipam:
                reduced_addresses_list.append(item)
    dictionary_used_ip[dmvpn_tunnel] = reduced_addresses_list
    # Write the updated IPAM file
    with open('DB/dmvpn_mgre_ipam.json', 'w') as outfile:
        json.dump(dictionary_used_ip, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    # # If VPC is a hub, remove address entries from dmvpn_tunnel_nhs_addresses.yml
    # import yaml
    # vpc_template = "dmvpn_hub"
    # dmvpn_tunnel = "1"
    # dmvpn_list_to_remove_from_ipam = ["10.255.0.4", "10.255.0.1"]

    reduced_tunnel_info_list = []
    if dmvpn_role == "dmvpn_hub":
        with open("DB/dmvpn_per_mgre_nhs_bgp_rr_address_info.yml", 'r') as yml_data:
            dictionary_initial_read = yaml.load(yml_data)
        print(dictionary_initial_read)
        for item in dictionary_initial_read['dmvpn_addresses'][dmvpn_tunnel]:
            if item['dmvpn_address'] not in dmvpn_list_to_remove_from_ipam:
                reduced_tunnel_info_list.append(item)
        print(reduced_tunnel_info_list)
        if not reduced_tunnel_info_list:
            del dictionary_initial_read['dmvpn_addresses'][dmvpn_tunnel]
        else:
            dictionary_initial_read['dmvpn_addresses'][dmvpn_tunnel] = reduced_tunnel_info_list
        print(dictionary_initial_read)

        # Write the new dmvpn_tunnel_nhs_addresses file
        with io.open('DB/dmvpn_per_mgre_nhs_bgp_rr_address_info.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(dictionary_initial_read, outfile, default_flow_style=False, allow_unicode=True)
    w = subprocess.Popen(['ansible-playbook', 'update_dmvpn_nhs_bgp_addresses.yml', '--extra-vars', 'target=csr1000v_aws', '-vvvv'], cwd="Ansible")
    w.wait()

    for eip in router_eips:
        subprocess.call("rm Ansible/host_vars/{}.json".format(eip), shell=True)
    w = subprocess.Popen(["terraform", "destroy"], cwd="VPCs/{}".format(vpc_number))
    w.wait()
    subprocess.call("rm -r VPCs/{}".format(vpc_number), shell=True)


def router_eips_get(vpc_number):
    router_eips = []
    with open('VPCs/{}/dmvpn_ip_addresses.auto.tfvars.json'.format(vpc_number)) as json_data:
        dictionary_tfvars = json.load(json_data)
    vpc_template = dictionary_tfvars['vpc_template']
    cloud_provider = dictionary_tfvars['cloud_provider']

    if cloud_provider == "aws":
        with open("VPCs/{}/terraform.tfstate".format(vpc_number)) as json_data:
            d = json.load(json_data)
            ip_a = d["modules"][0]["resources"]["aws_eip.CSR1000vA"]["primary"]["attributes"]["public_ip"]
            router_eips.append(ip_a)
            if vpc_template == "high_availability":
                ip_b = d["modules"][0]["resources"]["aws_eip.CSR1000vB"]["primary"]["attributes"]["public_ip"]
                router_eips.append(ip_b)

    if cloud_provider == "azure":
        with open("VPCs/{}/terraform.tfstate".format(vpc_number)) as json_data:
            d = json.load(json_data)
            ip_a = d["modules"][0]["resources"]["azurerm_public_ip.PIP1"]["primary"]["attributes"]["ip_address"]
            router_eips.append(ip_a)
            if vpc_template == "high_availability":
                ip_b = d["modules"][0]["resources"]["azurerm_public_ip.PIP2"]["primary"]["attributes"]["ip_address"]
                router_eips.append(ip_b)
    return router_eips


def vpc_number_get():
    while True:
        proceed = raw_input("\n\nWARNING - This program will destroy a VPC. This can not be undone without good backups and a lot of work. Do you want to proceed? Type 'yes' or 'no' and press [enter]: ")
        proceed = proceed.lower()
        proceed = proceed.strip()
        if proceed == "yes":
            break
        if proceed == "no":
            break
    if proceed == "no":
        return "exit"
    print "\n\nNote - these are your current VPCs"
    directories_os = os.listdir("VPCs")
    tempsortdir_oslist = []
    for dir_os in directories_os:
        tempsortdir_oslist.append(dir_os)
    tempsortdir_oslist.sort()
    for item in tempsortdir_oslist:
        print item
    while True:
        vpc_number = raw_input("\n\nWhich VPC number would you like to destroy? Please enter a number and press [enter]: ")
        vpc_number = int(vpc_number)
        if 1 <= vpc_number <= 4095:
            vpc_number = str(vpc_number)
            if vpc_number not in directories_os:
                print "VPC {} does not exist.".format(vpc_number)
            else:
                break
        else:
            print "\nTry again"

    return vpc_number


if __name__ == "__main__":
    main()