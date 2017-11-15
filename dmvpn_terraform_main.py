import simplejson as json
import os
import subprocess
import python_modules.vdss_ip_generation
import python_modules.terraform
import python_modules.dmvpn_ip_generation


def main():
    cidr_block = "10.0.0.0/21"
    cloud_provider = "aws"
    region = "us-west-1"
    availability_zone = "us-west-1a"
    availability_zone_ha = "us-west-1c"
    # vpc_template = dev, standard, high_availability
    vpc_template = 'high_availability'
    user_subnet_masks = 27
    csr1000v_instance_type = "c4.large"
    dmvpn_tunnel = "1"
    dmvpn_role = "dmvpn_spoke"
    path_var = os.environ["PATH"]
    path_var_plus = path_var + ":" + "/home/vagrant"
    os.environ["PATH"] = path_var_plus
    print(os.environ["PATH"])

    settings_dictionary = load_settings()
    licenseidtoken = settings_dictionary['smart_license']['licenseidtoken']
    email = settings_dictionary['smart_license']['email']
    dmvpn_key = settings_dictionary['keys']['dmvpn'][dmvpn_tunnel]
    vpc_number = vpc_number_get()
    subprocess.call(["mkdir", "VPCs/{}".format(vpc_number)])

    python_modules.terraform.terraform_tfvars_createfile(cloud_provider, vpc_number, settings_dictionary, region)
    python_modules.dmvpn_ip_generation.main(cidr_block, user_subnet_masks, region, csr1000v_instance_type, availability_zone, vpc_number, vpc_template, availability_zone_ha, licenseidtoken, email, dmvpn_tunnel, dmvpn_key)
    python_modules.terraform.dmvpn_create_definition_files(vpc_template, vpc_number, cloud_provider, dmvpn_role)
    python_modules.terraform.init_terraform(vpc_number)
#    python_modules.terraform.apply_terraform(vpc_number)

    #get EIP from tfstate
    #get RTB from tfstate
    #get ENI from tfstate
    #add RTB and ENI to tfvars.json and save in host_vars as {{host}}.json




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