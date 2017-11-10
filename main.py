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
    device_number_csr1000v_inside_ingress_count = 1
    device_number_csr1000v_inside_egress_count = 1
    device_number_csr1000v_outside_ingress_count = 1
    device_number_csr1000v_outside_egress_count = 1
    device_number_firewalls_count = 1

    settings_dictionary = load_settings()
    vpc_number = vpc_number_get()
    subprocess.call(["mkdir", "VPCs/{}".format(vpc_number)])
    python_modules.terraform.terraform_tfvars_createfile(cloud_provider, vpc_number, settings_dictionary, region)
    python_modules.vdss_ip_generation.main(cidr_block, region, availability_zone, vpc_number)
    python_modules.terraform.vdss_create_definition_files(vpc_number)
#    python_modules.terraform.init_terraform(vpc_number)
#    python_modules.terraform.apply_terraform(vpc_number)

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