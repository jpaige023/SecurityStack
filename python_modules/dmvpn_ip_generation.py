import simplejson as json
from netaddr import *
from copy import deepcopy


def main(cidr_block, user_subnet_masks, region, csr1000v_instance_type, availability_zone, vpc_number, vpc_template, availability_zone_ha, licenseidtoken, email, dmvpn_tunnel, dmvpn_key):
#    import simplejson as json
#    from netaddr import *
#    from copy import deepcopy
#    cidr_block = "10.0.0.0/21"
#    user_subnet_masks = 28
#    region = "us-west-1"
#    availability_zone = "us-west-1a"
#    vpc_number = 100
#    vpc_template = 'dev'

    dictionary_tfvars = {}
    if vpc_template == "dev":
        dictionary_tfvars = address_generation_dev(cidr_block, user_subnet_masks)
    elif vpc_template == "standard":
        dictionary_tfvars = address_generation_standard(cidr_block, user_subnet_masks)
    else:
        dictionary_tfvars = address_generation_high_availability(cidr_block, user_subnet_masks)

    dictionary_tfvars['region'] = region
    dictionary_tfvars['availability_zone'] = availability_zone
    dictionary_tfvars['cidr_block'] = cidr_block
    dictionary_tfvars['csr1000v_instance_type'] = csr1000v_instance_type
    dictionary_tfvars['vpc_number'] = vpc_number
    dictionary_tfvars['availability_zone_ha'] = availability_zone_ha
    dictionary_tfvars['licenseidtoken'] = licenseidtoken
    dictionary_tfvars['email'] = email
    dictionary_tfvars['dmvpn_tunnel'] = dmvpn_tunnel
    dictionary_tfvars['dmvpn_key'] = dmvpn_key

    # dmvpn_addresses = address_generation_DMVPN(vpc_number)
    # dictionary_tfvars.update(dmvpn_addresses)

    tunnel_address, tunnel_netmask = new_dmvpn_interface_address_assign(dmvpn_tunnel, vpc_number)
    tunnel_b_address = None
    if vpc_template == 'high_availability':
        tunnel_b_address = new_dmvpn_interface_address_assign(dmpvn_tunnel, vpc_number)
    dictionary_tfvars['tunnel_address'] = tunnel_address
    dictionary_tfvars['tunnel_b_address'] = tunnel_b_address
    dictionary_tfvars['tunnel_netmask'] = tunnel_netmask

    print(json.dumps(dictionary_tfvars, indent=4))

    with open('VPCs/{}/dmvpn_ip_addresses.auto.tfvars.json'.format(vpc_number), 'w') as outfile:
        json.dump(dictionary_tfvars, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    return dictionary_tfvars


# def address_generation_DMVPN(vpc_number):
#     """Generates DMVPN tunnel address based on VPC number provided
# First two octects are 10.254 12 bits for VPC number 4 bits for hosts
# router A's hostid = 0001
# router B's hostid = 0010
# :param str vpc_number: contains VPC number
# Returns
# :tunnel_address str ip address
# :tunnel_b_address str ip address
#     """
#     dmvpn_addresses = {}
#     vpc_number_int = int(vpc_number)
#     conversion = bin(vpc_number_int)
#     conversion_striped = conversion.lstrip('0b')
#     binary_length = len(conversion_striped)
#     ip_address_hostid = '0001'
#     ip_address_hostid_b = '0010'
#     if binary_length < 12:
#         binary_padding_number = 12 - binary_length
#         padding = ''
#         while binary_padding_number > 0:
#             padding = padding + '0'
#             binary_padding_number = binary_padding_number - 1
#         binary_sixteen_bits = padding + conversion_striped + ip_address_hostid
#         binary_sixteen_bits_b = padding + conversion_striped + ip_address_hostid_b
#     else:
#         binary_sixteen_bits = conversion_striped + ip_address_hostid
#         binary_sixteen_bits_b = conversion_striped + ip_address_hostid_b
#     octet_third = int(binary_sixteen_bits[0:8], 2)
#     octet_third = str(octet_third)
#     octet_fourth = int(binary_sixteen_bits[8:16], 2)
#     octet_fourth = str(octet_fourth)
#     octet_third_b = int(binary_sixteen_bits_b[0:8], 2)
#     octet_third_b = str(octet_third_b)
#     octet_fourth_b = int(binary_sixteen_bits_b[8:16], 2)
#     octet_fourth_b = str(octet_fourth_b)
#
#     tunnel_address = '10.254.' + octet_third + '.' + octet_fourth
#     dmvpn_addresses['tunnel_address'] = tunnel_address
#     tunnel_b_address = '10.254.' + octet_third_b + '.' + octet_fourth_b
#     dmvpn_addresses['tunnel_b_address'] = tunnel_b_address
#
#     return dmvpn_addresses


def address_generation_dev(cidr_block, user_subnet_masks):
#    from netaddr import *
#    cidr_block = "10.0.0.0/24"
#    user_subnet_masks = 28

    ip_addresses_dictionary = {}
    ip = IPNetwork(cidr_block)
    cidr_block_network_ID = ip.network
    cidr_block_network_ID = str(cidr_block_network_ID)
    ip_addresses_dictionary['cidr_block_network_ID'] = cidr_block_network_ID
    cidr_block_netmask = ip.netmask
    cidr_block_netmask = str(cidr_block_netmask)
    ip_addresses_dictionary['cidr_block_netmask'] = cidr_block_netmask
    subnets_routers = list(ip.subnet(28))
    router_a_subnet_g1 = subnets_routers[0]
    router_a_subnet_g1 = str(router_a_subnet_g1)
    ip_addresses_dictionary['router_a_subnet_g1'] = router_a_subnet_g1
    ips_router_a_g1 = IPNetwork(router_a_subnet_g1)
    router_a_address_g1 = ips_router_a_g1[4]
    router_a_address_g1 = str(router_a_address_g1)
    ip_addresses_dictionary['router_a_address_g1'] = router_a_address_g1
    ip_subnet_mask_g1 = IPNetwork(router_a_subnet_g1)
    router_a_subnet_mask_g1 = ip_subnet_mask_g1.netmask
    router_a_subnet_mask_g1 = str(router_a_subnet_mask_g1)
    ip_addresses_dictionary['router_a_subnet_mask_g1'] = router_a_subnet_mask_g1
    router_a_addressg1NH = ips_router_a_g1[1]
    router_a_addressg1NH = str(router_a_addressg1NH)
    ip_addresses_dictionary['router_a_addressg1NH'] = router_a_addressg1NH
    subnets_routers_g2 = list(ip.subnet(user_subnet_masks))
    router_a_subnet_g2 = subnets_routers_g2[1]
    router_a_subnet_g2 = str(router_a_subnet_g2)
    ip_addresses_dictionary['router_a_subnet_g2'] = router_a_subnet_g2
    ips_router_a_g2 = IPNetwork(router_a_subnet_g2)
    router_a_address_g2 = ips_router_a_g2[4]
    router_a_address_g2 = str(router_a_address_g2)
    ip_addresses_dictionary['router_a_address_g2'] = router_a_address_g2
    ip_subnet_mask_g2 = IPNetwork(router_a_subnet_g2)
    router_a_subnet_mask_g2 = ip_subnet_mask_g2.netmask
    router_a_subnet_mask_g2 = str(router_a_subnet_mask_g2)
    ip_addresses_dictionary['router_a_subnet_mask_g2'] = router_a_subnet_mask_g2
    router_a_addressg2NH = ips_router_a_g2[1]
    router_a_addressg2NH = str(router_a_addressg2NH)
    ip_addresses_dictionary['router_a_addressg2NH'] = router_a_addressg2NH
#    print(ip_addresses_dictionary)
    return ip_addresses_dictionary


def address_generation_standard(cidr_block, user_subnet_masks):
#    from netaddr import *
#    cidr_block = "10.0.0.0/24"
#    user_subnet_masks = 28
    cidr_block_list = [cidr_block]
    ip_addresses_dictionary = {}
    ip = IPNetwork(cidr_block)
    cidr_block_network_ID = ip.network
    cidr_block_network_ID = str(cidr_block_network_ID)
    ip_addresses_dictionary['cidr_block_network_ID'] = cidr_block_network_ID
    cidr_block_netmask = ip.netmask
    cidr_block_netmask = str(cidr_block_netmask)
    ip_addresses_dictionary['cidr_block_netmask'] = cidr_block_netmask
    subnets_routers = list(ip.subnet(28))
    router_a_subnet_g1 = subnets_routers[0]
    router_a_subnet_g1 = str(router_a_subnet_g1)
    ip_addresses_dictionary['router_a_subnet_g1'] = router_a_subnet_g1
    ips_router_a_g1 = IPNetwork(router_a_subnet_g1)
    router_a_address_g1 = ips_router_a_g1[4]
    router_a_address_g1 = str(router_a_address_g1)
    ip_addresses_dictionary['router_a_address_g1'] = router_a_address_g1
    ip_subnet_mask_g1 = IPNetwork(router_a_subnet_g1)
    router_a_subnet_mask_g1 = ip_subnet_mask_g1.netmask
    router_a_subnet_mask_g1 = str(router_a_subnet_mask_g1)
    ip_addresses_dictionary['router_a_subnet_mask_g1'] = router_a_subnet_mask_g1
    router_a_addressg1NH = ips_router_a_g1[1]
    router_a_addressg1NH = str(router_a_addressg1NH)
    ip_addresses_dictionary['router_a_addressg1NH'] = router_a_addressg1NH
    router_a_subnet_g2 = subnets_routers[1]
    router_a_subnet_g2 = str(router_a_subnet_g2)
    ip_addresses_dictionary['router_a_subnet_g2'] = router_a_subnet_g2
    ips_router_a_g2 = IPNetwork(router_a_subnet_g2)
    router_a_address_g2 = ips_router_a_g2[4]
    router_a_address_g2 = str(router_a_address_g2)
    ip_addresses_dictionary['router_a_address_g2'] = router_a_address_g2
    ip_subnet_mask_g2 = IPNetwork(router_a_subnet_g2)
    router_a_subnet_mask_g2 = ip_subnet_mask_g2.netmask
    router_a_subnet_mask_g2 = str(router_a_subnet_mask_g2)
    ip_addresses_dictionary['router_a_subnet_mask_g2'] = router_a_subnet_mask_g2
    router_a_addressg2NH = ips_router_a_g2[1]
    router_a_addressg2NH = str(router_a_addressg2NH)
    ip_addresses_dictionary['router_a_addressg2NH'] = router_a_addressg2NH
    cloud_address_space_set = IPSet(cidr_block_list)
    address_space_unavailable_list = [router_a_subnet_g1, router_a_subnet_g2]
    address_space_unavailable_set = IPSet(address_space_unavailable_list)
    unavailable = address_space_unavailable_set
    available = cloud_address_space_set ^ unavailable
    available_list = str(available)
    strip1 = available_list.lstrip('[IPSet(')
    strip2 = strip1.rstrip('])')
    split1 = strip2.split(',')
    split2 = []
    for item in split1:
        item1 = item.strip(" ")
        item2 = item1.strip("'")
        split2.append(item2)
    available_candidates = []
    for item in split2:
        ip = IPNetwork(item)
        subnets_available = list(ip.subnet(user_subnet_masks))
        available_candidates.extend(subnets_available)
    available_candidates_strs_list = []
    for item in available_candidates:
        item1 = str(item)
        available_candidates_strs_list.append(item1)
    users_subnet_a = available_candidates_strs_list[0]
    ip_addresses_dictionary['users_subnet_a'] = users_subnet_a
#    print(ip_addresses_dictionary)
    return ip_addresses_dictionary


def address_generation_high_availability(cidr_block, user_subnet_masks):
#    from netaddr import *
#    cidr_block = "10.0.0.0/24"
#    user_subnet_masks = 28
    ip_addresses_dictionary = {}
    cidr_block_list = [cidr_block]
    ip = IPNetwork(cidr_block)
    cidr_block_network_ID = ip.network
    cidr_block_network_ID = str(cidr_block_network_ID)
    ip_addresses_dictionary['cidr_block_network_ID'] = cidr_block_network_ID
    cidr_block_netmask = ip.netmask
    cidr_block_netmask = str(cidr_block_netmask)
    ip_addresses_dictionary['cidr_block_netmask'] = cidr_block_netmask
    subnets_routers = list(ip.subnet(28))
    router_a_subnet_g1 = subnets_routers[0]
    router_a_subnet_g1 = str(router_a_subnet_g1)
    ip_addresses_dictionary['router_a_subnet_g1'] = router_a_subnet_g1
    ips_router_a_g1 = IPNetwork(router_a_subnet_g1)
    router_a_address_g1 = ips_router_a_g1[4]
    router_a_address_g1 = str(router_a_address_g1)
    ip_addresses_dictionary['router_a_address_g1'] = router_a_address_g1
    ip_subnet_mask_g1 = IPNetwork(router_a_subnet_g1)
    router_a_subnet_mask_g1 = ip_subnet_mask_g1.netmask
    router_a_subnet_mask_g1 = str(router_a_subnet_mask_g1)
    ip_addresses_dictionary['router_a_subnet_mask_g1'] = router_a_subnet_mask_g1
    router_a_addressg1NH = ips_router_a_g1[1]
    router_a_addressg1NH = str(router_a_addressg1NH)
    ip_addresses_dictionary['router_a_addressg1NH'] = router_a_addressg1NH
    router_a_subnet_g2 = subnets_routers[1]
    router_a_subnet_g2 = str(router_a_subnet_g2)
    ip_addresses_dictionary['router_a_subnet_g2'] = router_a_subnet_g2
    ips_router_a_g2 = IPNetwork(router_a_subnet_g2)
    router_a_address_g2 = ips_router_a_g2[4]
    router_a_address_g2 = str(router_a_address_g2)
    ip_addresses_dictionary['router_a_address_g2'] = router_a_address_g2
    ip_subnet_mask_g2 = IPNetwork(router_a_subnet_g2)
    router_a_subnet_mask_g2 = ip_subnet_mask_g2.netmask
    router_a_subnet_mask_g2 = str(router_a_subnet_mask_g2)
    ip_addresses_dictionary['router_a_subnet_mask_g2'] = router_a_subnet_mask_g2
    router_a_addressg2NH = ips_router_a_g2[1]
    router_a_addressg2NH = str(router_a_addressg2NH)
    ip_addresses_dictionary['router_a_addressg2NH'] = router_a_addressg2NH
    router_b_subnet_g1 = subnets_routers[2]
    router_b_subnet_g1 = str(router_b_subnet_g1)
    ip_addresses_dictionary['router_b_subnet_g1'] = router_b_subnet_g1
    ips_router_b_g1 = IPNetwork(router_b_subnet_g1)
    router_b_address_g1 = ips_router_b_g1[4]
    router_b_address_g1 = str(router_b_address_g1)
    ip_addresses_dictionary['router_b_address_g1'] = router_b_address_g1
    ip_subnet_mask_rb_g1 = IPNetwork(router_b_subnet_g1)
    router_b_subnet_mask_g1 = ip_subnet_mask_rb_g1.netmask
    router_b_subnet_mask_g1 = str(router_b_subnet_mask_g1)
    ip_addresses_dictionary['router_b_subnet_mask_g1'] = router_b_subnet_mask_g1
    router_b_addressg1NH = ips_router_b_g1[1]
    router_b_addressg1NH = str(router_b_addressg1NH)
    ip_addresses_dictionary['router_b_addressg1NH'] = router_b_addressg1NH
    router_b_subnet_g2 = subnets_routers[3]
    router_b_subnet_g2 = str(router_b_subnet_g2)
    ip_addresses_dictionary['router_b_subnet_g2'] = router_b_subnet_g2
    ips_router_b_g2 = IPNetwork(router_b_subnet_g2)
    router_b_address_g2 = ips_router_b_g2[4]
    router_b_address_g2 = str(router_b_address_g2)
    ip_addresses_dictionary['router_b_address_g2'] = router_b_address_g2
    ip_subnet_mask_rb_g2 = IPNetwork(router_b_subnet_g2)
    router_b_subnet_mask_g2 = ip_subnet_mask_rb_g2.netmask
    router_b_subnet_mask_g2 = str(router_b_subnet_mask_g2)
    ip_addresses_dictionary['router_b_subnet_mask_g2'] = router_b_subnet_mask_g2
    router_b_addressg2NH = ips_router_b_g2[1]
    router_b_addressg2NH = str(router_b_addressg2NH)
    ip_addresses_dictionary['router_b_addressg2NH'] = router_b_addressg2NH
    cloud_address_space_set = IPSet(cidr_block_list)
    address_space_unavailable_list = [router_a_subnet_g1, router_a_subnet_g2, router_b_subnet_g1,
                                      router_b_subnet_g2]
    address_space_unavailable_set = IPSet(address_space_unavailable_list)
    unavailable = address_space_unavailable_set
    available = cloud_address_space_set ^ unavailable
    available_list = str(available)
    strip1 = available_list.lstrip('[IPSet(')
    strip2 = strip1.rstrip('])')
    split1 = strip2.split(',')
    split2 = []
    for item in split1:
        item1 = item.strip(" ")
        item2 = item1.strip("'")
        split2.append(item2)
    available_candidates = []
    for item in split2:
        ip = IPNetwork(item)
        subnets_available = list(ip.subnet(user_subnet_masks))
        available_candidates.extend(subnets_available)
    available_candidates_strs_list = []
    for item in available_candidates:
        item1 = str(item)
        available_candidates_strs_list.append(item1)
    users_subnet_a = available_candidates_strs_list[0]
    ip_addresses_dictionary['users_subnet_a'] = users_subnet_a
    users_subnet_b = available_candidates_strs_list[1]
    ip_addresses_dictionary['users_subnet_b'] = users_subnet_b
#    print(ip_addresses_dictionary)
    return ip_addresses_dictionary


def cloud_address_space_get():
    # This returns a list of all cloud address space
    # import simplejson as json
    with open('DB/cloud_space.json') as json_data:
        dictionary = json.load(json_data)
    cloud_address_space_list = dictionary['cloud_space']
    return cloud_address_space_list


def dmvpn_interface_address_space_get():
    # This returns list of tunnel space dictionaries
    # import simplejson as json
    with open('DB/dmvpn_interface_address_space.json') as json_data:
        dictionary = json.load(json_data)
    dmvpn_interface_address_space = dictionary['dmvpn_tunnel_address_space']
    dmvpn_interface_address_space_list = []
    for item in dmvpn_interface_address_space:
        dmvpn_interface_address_space_list.extend(item.values())
    return dmvpn_interface_address_space_list


def new_dmvpn_interface_address_assign(dmvpn_tunnel, vpc_number):
    # Returns first available dmvpn address space per tunnel ipam and notes as used
    # from netaddr import *
    # import simplejson as json
    # dmvpn_tunnel = "1"
    # vpc_number = "100"

    # Get the IP range for dmvpn_tunnel
    with open('DB/dmvpn_interface_address_space.json') as json_data:
        dictionary_dmvpn_interface_address_space = json.load(json_data)
    dmvpn_interface_address_space_list = dictionary_dmvpn_interface_address_space['dmvpn_tunnel_address_space']
    for item in dmvpn_interface_address_space_list:
            for key, value in item.iteritems():
                if key == dmvpn_tunnel:
                    tunnel_cidr = value
    # print tunnel_cidr

    # Get used addresses in IP range for dmvpn tunnel interface
    with open('DB/dmvpn_tunnel_ipam.json') as json_data:
        dictionary_used_ip = json.load(json_data)
    addresses_used_list = dictionary_used_ip[dmvpn_tunnel]
    full_used_addresses_list = []
    for item in addresses_used_list:
            for key in item:
                full_used_addresses_list.append(key)
    # print full_used_addresses_list

    possible_ip_list = []
    ip1 = IPNetwork(tunnel_cidr)
    tunnel_netmask = str(ip1.netmask)
    for ip in IPNetwork(tunnel_cidr):
        if ip != ip1.network:
            if ip != ip1.broadcast:
                ip_str = str(ip)
                possible_ip_list.append(ip_str)
    # print possible_ip_list

    for ip in possible_ip_list:
        ip_str = str(ip)
        if ip_str not in full_used_addresses_list:
            dmvpn_address = ip_str
            break
    # print dmvpn_address
    # print addresses_used_list

    # Save new assigned dmvpn_address to dmvpn_tunnel_ipam
    new_dmvpn_dict = {dmvpn_address: vpc_number}
    addresses_used_list.append(new_dmvpn_dict)
    dictionary_used_ip[dmvpn_tunnel] = addresses_used_list
    with open('DB/dmvpn_tunnel_ipam.json', 'w') as outfile:
        json.dump(dictionary_used_ip, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    # print dmvpn_address, tunnel_netmask
    return dmvpn_address, tunnel_netmask


def vpc_address_space_in_use_get():
    # This returns a list of all vpc address space being used
    # import simplejson as json
    with open('DB/vpc_cidr.json') as json_data:
        dictionary = json.load(json_data)
    vpc_address_space_in_use_list = dictionary.values()
    return vpc_address_space_in_use_list


def find_space_available(cloud_address_space_list, vpc_address_space_in_use_list, dmvpn_interface_address_space_list, subnet_mask_proposed):
    # from netaddr import *
    # from copy import deepcopy
    # cloud_address_space_list = ['10.0.0.0/24']
    # subnet_mask_proposed = 27
    # vpc_address_space_in_use_list = ['10.0.0.0/28', '10.0.0.64/27']
    # dmvpn_interface_address_space_list = ['10.0.0.224/27', '10.1.1.224/27']

    cloud_address_space_list_temp = deepcopy(cloud_address_space_list)
    cloud_address_space_list_temp.extend(dmvpn_interface_address_space_list)
    cloud_address_space_set = IPSet(cloud_address_space_list_temp)
    address_space_unavailable = dmvpn_interface_address_space_list
    address_space_unavailable_set = IPSet(address_space_unavailable)
    vpc_address_space_in_use_set = IPSet(vpc_address_space_in_use_list)
    unavailable = address_space_unavailable_set | vpc_address_space_in_use_set
    available = cloud_address_space_set ^ unavailable
    available_list = str(available)
    strip1 = available_list.lstrip('[IPSet(')
    strip2 = strip1.rstrip('])')
    split1 = strip2.split(',')
    split2 = []
    for item in split1:
        item1 = item.strip(" ")
        item2 = item1.strip("'")
        split2.append(item2)
    full_subnets_available_list = []
    for item in split2:
        ip = IPNetwork(item)
        subnets_available = list(ip.subnet(subnet_mask_proposed))
        subnets_available_list = list(subnets_available)
        for item in subnets_available_list:
            item = str(item)
            full_subnets_available_list.append(item)
    print full_subnets_available_list


def vpc_cidr_candidate_availability_check(cidr_block, vpc_address_space_in_use_list, dmvpn_interface_address_space_list):
    # from copy import deepcopy
    # from netaddr import *
    # cidr_block = '10.0.0.96/27'
    # cloud_address_space_list = ['10.0.0.0/24']
    # vpc_address_space_in_use_list = ['10.0.0.0/28', '10.0.0.64/26']
    # dmvpn_interface_address_space_list = ['10.0.0.224/27', '10.1.1.224/27']

    cidr_block_list_temp = [cidr_block]
    address_space_unavailable = deepcopy(vpc_address_space_in_use_list)
    address_space_unavailable.extend(dmvpn_interface_address_space_list)
    cidr_block_values_set = IPSet(address_space_unavailable)
    network_candidate_set = IPSet(cidr_block_list_temp)
    result1 = network_candidate_set.issubset(cidr_block_values_set)
    result2 = False
    for block in address_space_unavailable:
        block_temp_list = [block]
        block_temp_set = IPSet(block_temp_list)
        result2 = network_candidate_set.issuperset(block_temp_set)
        if result2 == True:
            break
    if cidr_block in address_space_unavailable:
        result = ['not available', '{} is already in use'.format(cidr_block)]
    elif result1:
        result = ['not available', '{} is a subset of a used CIDR block'.format(cidr_block)]
    elif result2:
        result = ['not available', '{} is a superset containing a used CIDR block'.format(cidr_block)]
    else:
        result = ['available']
    return result



if __name__ == "__main__":
   main()