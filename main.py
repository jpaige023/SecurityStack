import simplejson as json
import re
import subprocess
from subprocess import Popen, PIPE
import python_modules.vdss_ip_generation
import python_modules.terraform
import os

def main():
    cidr_block = "10.0.0.0/21"
    cloud_provider = "aws"
    region = "us-west-1"
    availability_zone = "us-west-1a"
    device_number_csr1000v_inside_ingress_count = 5
    device_number_csr1000v_inside_egress_count = 1
    device_number_csr1000v_outside_ingress_count = 1
    device_number_csr1000v_outside_egress_count = 1
    device_number_firewalls_count = 1

    settings_dictionary = load_settings()
    vpc_number = vpc_number_get()
    subprocess.call(["mkdir", "VPCs/{}".format(vpc_number)])
    python_modules.terraform.terraform_tfvars_createfile(cloud_provider, vpc_number, settings_dictionary, region)
    python_modules.vdss_ip_generation.main(cidr_block, region, availability_zone, vpc_number)
    # copy terraform modules
    subprocess.call(
        "cp -a TEMPLATES/Cloud/{}/vpc_security_stack/modules VPCs/{}".format(cloud_provider.upper(), vpc_number),
        shell=True)
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/vpc_security_stack/aws.tf VPCs/{}".format(cloud_provider.upper(), vpc_number),
        shell=True)
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/vpc_security_stack/vpc_base_0.tf VPCs/{}".format(cloud_provider.upper(), vpc_number),
        shell=True)
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/vpc_security_stack/bastion_0.tf VPCs/{}".format(cloud_provider.upper(), vpc_number),
        shell=True)
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/vpc_security_stack/controller_0.tf VPCs/{}".format(cloud_provider.upper(), vpc_number),
        shell=True)

    # csr1000v inside ingress
    device_number_csr1000v_inside_ingress_counter = 0
    while device_number_csr1000v_inside_ingress_counter != device_number_csr1000v_inside_ingress_count:
        device_number_csr1000v_inside_ingress = str(device_number_csr1000v_inside_ingress_counter)
        replacements = {'XXXXX': device_number_csr1000v_inside_ingress}
        with open("TEMPLATES/Cloud/{}/vpc_security_stack/csr1000v_inside_ingress_0.tf".format(cloud_provider.upper())) as infile, open(
                "VPCs/{}/csr1000v_inside_ingress_{}.tf".format(vpc_number, device_number_csr1000v_inside_ingress), 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
        device_number_csr1000v_inside_ingress_counter = device_number_csr1000v_inside_ingress_counter + 1

    # csr1000v inside egress
    device_number_csr1000v_inside_egress_counter = 0
    while device_number_csr1000v_inside_egress_counter != device_number_csr1000v_inside_egress_count:
        device_number_csr1000v_inside_egress = str(device_number_csr1000v_inside_egress_counter)
        replacements = {'XXXXX': device_number_csr1000v_inside_egress}
        with open("TEMPLATES/Cloud/{}/vpc_security_stack/csr1000v_inside_egress_0.tf".format(cloud_provider.upper())) as infile, open(
                "VPCs/{}/csr1000v_inside_egress_{}.tf".format(vpc_number, device_number_csr1000v_inside_egress), 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
        device_number_csr1000v_inside_egress_counter = device_number_csr1000v_inside_egress_counter + 1

    # csr1000v outside ingress
    device_number_csr1000v_outside_ingress_counter = 0
    while device_number_csr1000v_outside_ingress_counter != device_number_csr1000v_outside_ingress_count:
        device_number_csr1000v_outside_ingress = str(device_number_csr1000v_outside_ingress_counter)
        replacements = {'XXXXX': device_number_csr1000v_outside_ingress}
        with open("TEMPLATES/Cloud/{}/vpc_security_stack/csr1000v_outside_ingress_0.tf".format(cloud_provider.upper())) as infile, open(
                "VPCs/{}/csr1000v_outside_ingress_{}.tf".format(vpc_number, device_number_csr1000v_outside_ingress), 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
        device_number_csr1000v_outside_ingress_counter = device_number_csr1000v_outside_ingress_counter + 1

    # csr1000v outside egress
    device_number_csr1000v_outside_egress_counter = 0
    while device_number_csr1000v_outside_egress_counter != device_number_csr1000v_outside_egress_count:
        device_number_csr1000v_outside_egress = str(device_number_csr1000v_outside_egress_counter)
        replacements = {'XXXXX': device_number_csr1000v_outside_egress}
        with open("TEMPLATES/Cloud/{}/vpc_security_stack/csr1000v_outside_egress_0.tf".format(cloud_provider.upper())) as infile, open(
                "VPCs/{}/csr1000v_outside_egress_{}.tf".format(vpc_number, device_number_csr1000v_outside_egress), 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
        device_number_csr1000v_outside_egress_counter = device_number_csr1000v_outside_egress_counter + 1

    # firewalls
    device_number_firewalls_counter = 0
    while device_number_firewalls_counter != device_number_firewalls_count:
        device_number_firewalls = str(device_number_firewalls_counter)
        replacements = {'XXXXX': device_number_firewalls}
        with open("TEMPLATES/Cloud/{}/vpc_security_stack/firewalls_0.tf".format(cloud_provider.upper())) as infile, open(
                "VPCs/{}/firewalls_{}.tf".format(vpc_number, device_number_firewalls), 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
    device_number_firewalls_counter = device_number_firewalls_counter + 1


def load_settings():
    with open("Settings/settings.json") as settings_json_data:
        settings_dictionary = json.load(settings_json_data)
    return settings_dictionary


def vpc_number_get():
    print "\n\nNote these are your current VPCs"
    directories_os = os.listdir("VPCs")
    for dir_os in directories_os:
        print dir_os
    while True:
        vpc_number = raw_input("\n\nFor your new VPC, enter an unused number between 1 and 4095 and press [enter]: ")
        vpc_number = int(vpc_number)
        if 1 <= vpc_number <= 4095:
            vpc_number = str(vpc_number)
            if vpc_number in directories_os:
                print vpc_number
                print "\nThis VPC number is already in use."
            else:
                break
        else:
            print "\nYou did not pick a number between 1 and 4095. Try again"
    return vpc_number


if __name__ == "__main__":
    main()