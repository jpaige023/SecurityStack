from netaddr import *
import simplejson as json

def main(cidr_block, region, availability_zone, vpc_number):
    """Needs input of CIDR block, region, availability, zone. Note CIDR block must be a /21 or larger"""
#    cidr_block = "10.0.0.0/21"
#    region = "us-west-1"
#    availability_zone = "us-west-1a"

    vdss_subnets = vdss_subnets_generation(cidr_block)

    vdss_cidr_networkid_netmask = vpc_cidr_networkid_netmask_generation(cidr_block)

    vdss_ip_addresses = vdss_ip_address_generation(vdss_subnets)

    print(json.dumps(vdss_ip_addresses, indent=4))
    print(vdss_ip_addresses['ftd_general_31_e3'])

    dictionary_tfvars = {}

    dictionary_tfvars.update(vdss_ip_addresses)
    dictionary_tfvars.update(vdss_subnets)

    dictionary_tfvars['region'] = region
    dictionary_tfvars['availability_zone'] = availability_zone
    dictionary_tfvars['cidr_block'] = cidr_block


    with open('VPCs/{}/vdss_ip_addresses.auto.tfvars.json'.format(vpc_number), 'w') as outfile:
        json.dump(dictionary_tfvars, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)


def vdss_ip_address_generation(vdss_subnets):
#    from netaddr import *
#    vdss_subnets = {}
#    vdss_subnets['subnet_public'] = "172.31.0.0/24"
#    vdss_subnets['subnet_management'] = "172.31.1.0/24"
#    vdss_subnets['subnet_inside_csr_fw'] = "172.31.4.0/24"
#    vdss_subnets['subnet_asav_ftd'] = "172.31.3.0/24"
#    vdss_subnets['subnet_outside_csr_fw'] = "172.31.2.0/24"

    ip_public = IPNetwork(vdss_subnets['subnet_public'])
    ip_management = IPNetwork(vdss_subnets['subnet_management'])
    ip_asav_ftd = IPNetwork(vdss_subnets['subnet_asav_ftd'])
    ip_outside_csr_fw = IPNetwork(vdss_subnets['subnet_outside_csr_fw'])
    ip_inside_csr_fw = IPNetwork(vdss_subnets['subnet_inside_csr_fw'])


    vdss_addresses = {}
    # Generate all csr1000v_inside_egress addresses
    counter = 0
    while counter != 6:
        strcounter = str(counter)

        e0 = 'csr1000v_inside_egress_' + strcounter + '_e0'
        tempaddress = ip_public[counter + 4]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'csr1000v_inside_egress_' + strcounter + '_e1'
        tempaddress = ip_inside_csr_fw[counter + 4]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'csr1000v_inside_egress_' + strcounter + "_e2"
        tempaddress = ip_management[counter + 4]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        counter = counter + 1


    # Generate FMC ip
    counter = 0
    e0 = 'fmc' + '_e0'
    tempaddress = ip_management[counter + 14]
    tempaddress = str(tempaddress)
    vdss_addresses[e0] = tempaddress

    # Generate bastion ips
    counter = 0
    e0 = 'bastion' + '_e0'
    tempaddress = ip_public[counter + 15]
    tempaddress = str(tempaddress)
    vdss_addresses[e0] = tempaddress

    e1 = 'bastion' + '_e1'
    tempaddress = ip_management[counter + 15]
    tempaddress = str(tempaddress)
    vdss_addresses[e1] = tempaddress

    # Generate all csr1000v_outside_egress addresses
    counter = 0
    while counter != 6:
        strcounter = str(counter)

        e0 = 'csr1000v_outside_egress_' + strcounter + '_e0'
        tempaddress = ip_public[counter + 16]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'csr1000v_outside_egress_' + strcounter + '_e1'
        tempaddress = ip_outside_csr_fw[counter + 16]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'csr1000v_outside_egress_' + strcounter + "_e2"
        tempaddress = ip_management[counter + 16]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        counter = counter + 1

    # Generate ansible_controller
    counter = 0
    e0 = 'controller' + '_e0'
    tempaddress = ip_management[counter + 22]
    tempaddress = str(tempaddress)
    vdss_addresses[e0] = tempaddress

    e1 = 'controller' + '_e1'
    tempaddress = ip_inside_csr_fw[counter + 22]
    tempaddress = str(tempaddress)
    vdss_addresses[e1] = tempaddress

    # Generate all csr1000v_inside_ingress addresses
    while counter != 32:
        strcounter = str(counter)

        e0 = 'csr1000v_inside_ingress_' + strcounter + '_e0'
        tempaddress = ip_public[counter + 32]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'csr1000v_inside_ingress_' + strcounter + '_e1'
        tempaddress = ip_inside_csr_fw[counter + 32]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'csr1000v_inside_ingress_' + strcounter + "_e2"
        tempaddress = ip_management[counter + 32]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        counter = counter + 1


    # Generate all asav addresses
    counter = 0
    while counter != 32:
        strcounter = str(counter)

        e0 = 'asav_general_' + strcounter + '_e0'
        tempaddress = ip_management[counter + 64]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'asav_general_' + strcounter + '_e1'
        tempaddress = ip_outside_csr_fw[counter + 64]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'asav_general_' + strcounter + "_e2"
        tempaddress = ip_asav_ftd[counter + 64]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        counter = counter + 1

    # Generate all ftd addresses
    counter = 0
    while counter != 32:
        strcounter = str(counter)

        e0 = 'ftd_general_' + strcounter + '_e0'
        tempaddress = ip_management[counter + 96]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'ftd_general_' + strcounter + '_e1'
        tempaddress = ip_management[counter + 128]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'ftd_general_' + strcounter + '_e2'
        tempaddress = ip_inside_csr_fw[counter + 96]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        e3 = 'ftd_general_' + strcounter + "_e3"
        tempaddress = ip_asav_ftd[counter + 96]
        tempaddress = str(tempaddress)
        vdss_addresses[e3] = tempaddress

        counter = counter + 1

    # Generate all csr1000v_outside_ingress addresses
    counter = 0
    while counter != 32:
        strcounter = str(counter)

        e0 = 'csr1000v_outside_ingress_' + strcounter + '_e0'
        tempaddress = ip_public[counter + 192]
        tempaddress = str(tempaddress)
        vdss_addresses[e0] = tempaddress

        e1 = 'csr1000v_outside_ingress_' + strcounter + '_e1'
        tempaddress = ip_outside_csr_fw[counter + 192]
        tempaddress = str(tempaddress)
        vdss_addresses[e1] = tempaddress

        e2 = 'csr1000v_outside_ingress_' + strcounter + "_e2"
        tempaddress = ip_management[counter + 192]
        tempaddress = str(tempaddress)
        vdss_addresses[e2] = tempaddress

        counter = counter + 1

    return vdss_addresses


def vdss_subnets_generation(cidr_block):
    ip = IPNetwork(cidr_block)
    subnets_24 = list(ip.subnet(24))
    subnet_public = subnets_24[0]
    subnet_management = subnets_24[1]
    subnet_outside_csr_fw = subnets_24[2]
    subnet_asav_ftd = subnets_24[3]
    subnet_inside_csr_fw = subnets_24[4]

    subnet_public = str(subnet_public)
    subnet_management = str(subnet_management)
    subnet_asav_ftd = str(subnet_asav_ftd)
    subnet_outside_csr_fw = str(subnet_outside_csr_fw)
    subnet_inside_csr_fw = str(subnet_inside_csr_fw)

    vpc_subnets = {}
    vpc_subnets['subnet_public'] = subnet_public
    vpc_subnets['subnet_management'] = subnet_management
    vpc_subnets['subnet_asav_ftd'] = subnet_asav_ftd
    vpc_subnets['subnet_outside_csr_fw'] = subnet_outside_csr_fw
    vpc_subnets['subnet_inside_csr_fw'] = subnet_inside_csr_fw

    return vpc_subnets


def vpc_cidr_networkid_netmask_generation(cidr_block):
    ip = IPNetwork(cidr_block)
    vpc_cidr_block_network_ID = ip.network
    vpc_cidr_block_netmask = ip.netmask

    vpc_cidr_block_network_ID = str(vpc_cidr_block_network_ID)
    vpc_cidr_block_netmask = str(vpc_cidr_block_netmask)

    vpc_cidr_networkid_netmask = {}
    vpc_cidr_networkid_netmask['vpc_cidr_block_network_ID'] = vpc_cidr_block_network_ID
    vpc_cidr_networkid_netmask['vpc_cidr_block_netmask'] = vpc_cidr_block_netmask

    return vpc_cidr_networkid_netmask


if __name__ == "__main__":
   main()