import simplejson as json
from netaddr import *
from copy import deepcopy


def address_generation_DMVPN(vpc_number):
    """Generates DMVPN tunnel address based on VPC number provided
First two octects are 10.254 12 bits for VPC number 4 bits for hosts
router A's hostid = 0001
router B's hostid = 0010
:param str vpc_number: contains VPC number
Returns
:tunnel_address str ip address
:tunnel_b_address str ip address
    """
    vpc_number_int = int(vpc_number)
    conversion = bin(vpc_number_int)
    conversion_striped = conversion.lstrip('0b')
    binary_length = len(conversion_striped)
    ip_address_hostid = '0001'
    ip_address_hostid_b = '0010'
    if binary_length < 12:
        binary_padding_number = 12 - binary_length
        padding = ''
        while binary_padding_number > 0:
            padding = padding + '0'
            binary_padding_number = binary_padding_number - 1
        binary_sixteen_bits = padding + conversion_striped + ip_address_hostid
        binary_sixteen_bits_b = padding + conversion_striped + ip_address_hostid_b
    else:
        binary_sixteen_bits = conversion_striped + ip_address_hostid
        binary_sixteen_bits_b = conversion_striped + ip_address_hostid_b
    octet_third = int(binary_sixteen_bits[0:8], 2)
    octet_third = str(octet_third)
    octet_fourth = int(binary_sixteen_bits[8:16], 2)
    octet_fourth = str(octet_fourth)
    octet_third_b = int(binary_sixteen_bits_b[0:8], 2)
    octet_third_b = str(octet_third_b)
    octet_fourth_b = int(binary_sixteen_bits_b[8:16], 2)
    octet_fourth_b = str(octet_fourth_b)

    tunnel_address = '10.254.' + octet_third + '.' + octet_fourth
    tunnel_b_address = '10.254.' + octet_third_b + '.' + octet_fourth_b

    return tunnel_address, tunnel_b_address


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


def address_generation_az_single(cidr_block, user_subnet_masks):
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



def address_generation_az_double(cidr_block, user_subnet_masks):
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
    f = open("Settings/cloud_address_space", "r")
    cloud_address_space = f.readlines()
    f.close()
    cloud_address_space_clean = []
    for item in cloud_address_space:
        item_striped = item.rstrip("\n")
        cloud_address_space_clean.append(item_striped)
    return cloud_address_space_clean


def vpc_address_space_in_use_get():
#    import simplejson as json
    with open('SecurityPolicies/VPCandCIDRdictionary.json') as json_data:
        dictionary = json.load(json_data)
    vpc_address_space_in_use = dictionary.values()
    return vpc_address_space_in_use


def space_available(cloud_address_space, vpc_address_space_in_use, subnet_mask_proposed):
#    from netaddr import *
#    cloud_address_space = ['10.0.0.0/8']
#    subnet_mask_proposed = 24
#    vpc_address_space_in_use = []
    cloud_address_space_set = IPSet(cloud_address_space)
    address_space_unavailable = ['10.254.0.0/16']
    address_space_unavailable_set = IPSet(address_space_unavailable)
    vpc_address_space_in_use_set = IPSet(vpc_address_space_in_use)
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


def vpc_cidr_candidate_availability_check(network_new_candidate, vpc_address_space_in_use):
#    from copy import deepcopy
#    from netaddr import *
#    network_new_candidate = '10.1.128.0/28'
#    vpc_address_space_in_use = ['10.1.129.0/30', '10.1.128.0/24']
#    print vpc_address_space_in_use
    network_new_candidate_list_temp = [network_new_candidate]
    address_space_unavailable = deepcopy(vpc_address_space_in_use)
    address_space_unavailable.append('10.254.0.0/16')
    cidr_block_values_set = IPSet(address_space_unavailable)
    network_candidate_set = IPSet(network_new_candidate_list_temp)
    result1 = network_candidate_set.issubset(cidr_block_values_set)
    result2 = False
    for block in address_space_unavailable:
        block_temp_list = [block]
        block_temp_set = IPSet(block_temp_list)
        result2 = network_candidate_set.issuperset(block_temp_set)
        if result2 == True:
            break
    if network_new_candidate in address_space_unavailable:
        result = ['not available', '{} is already in use'.format(network_new_candidate)]
    elif result1:
        result = ['not available', '{} is a subset of a used CIDR block'.format(network_new_candidate)]
    elif result2:
        result = ['not available', '{} is a superset containing a used CIDR block'.format(network_new_candidate)]
    else:
        result = ['available']
    return result
