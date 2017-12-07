import simplejson as json
import os
import subprocess
import python_modules.vdss_ip_generation
import python_modules.terraform
import python_modules.dmvpn_ip_generation
import python_modules.ansible_hosts
import python_modules.dmvpn_hub_create
import python_modules.azure_ha


def main():
    # Receive or input variables
    cidr_block = "10.0.170.0/24"
    # aws or azure
    cloud_provider = "aws"
    # us-east-1, us-east-2, us-west-1, us-west-2
    # East US, West US
    region = "us-west-2"
    # for aws only
    availability_zone = "us-west-2a"
    availability_zone_ha = "us-west-2c"
    # vpc_template = dev, standard, high_availability
    vpc_template = 'dev'
    user_subnet_masks = 28
    # c4.large
    # standard_d2_v2
    csr1000v_instance_type = "c4.large"
    dmvpn_tunnel = "1"
    # dmvpn_role = "dmvpn_spoke" or "dmvpn_hub"
    dmvpn_role = "dmvpn_hub"

    # For Pycharm change PATH to find Terraform
    path_var = os.environ["PATH"]
    path_var_plus = path_var + ":" + "/home/vagrant"
    os.environ["PATH"] = path_var_plus

    # Is cidr_block in available_space?

    # Is cidr_block already in use? If not add entry to vpc_cidr.json


    # Gather Settings and Information
    settings_dictionary = load_settings()
    licenseidtoken = settings_dictionary['smart_license']['licenseidtoken']
    email = settings_dictionary['smart_license']['email']
    dmvpn_key = settings_dictionary['keys']['dmvpn'][dmvpn_tunnel]
    vpc_number = vpc_number_get()
    default_user = None
    default_password = None
    subscription_id = None
    api_client_id = None
    api_client_secret = None
    tenant_id = None
    network_contributor_role_id = None
    router_app_object_id = None
    router_app_principal_id = None
    router_app_key = None
    if cloud_provider == 'azure':
        default_user = settings_dictionary['keys']['cloud']['azure']['default_user']
        default_password = settings_dictionary['keys']['cloud']['azure']['default_password']
        subscription_id = settings_dictionary['keys']['cloud']['azure']['subscription_id']
        api_client_id = settings_dictionary['keys']['cloud']['azure']['api_client_id']
        api_client_secret = settings_dictionary['keys']['cloud']['azure']['api_client_secret']
        tenant_id = settings_dictionary['keys']['cloud']['azure']['tenant_id']
        network_contributor_role_id = settings_dictionary['keys']['cloud']['azure']['network_contributor_role_id']
        router_app_object_id = settings_dictionary['keys']['cloud']['azure']['router_app_object_id']
        router_app_principal_id = settings_dictionary['keys']['cloud']['azure']['router_app_principal_id']
        router_app_key = settings_dictionary['keys']['cloud']['azure']['router_app_key']

    # Create Cloud Directory
    subprocess.call(["mkdir", "VPCs/{}".format(vpc_number)])
    python_modules.terraform.terraform_tfvars_createfile(cloud_provider, vpc_number, settings_dictionary, region)

    # Generate Variables
    dictionary_tfvars = python_modules.dmvpn_ip_generation.main(cloud_provider, cidr_block, user_subnet_masks, region, csr1000v_instance_type, availability_zone, vpc_number, vpc_template, availability_zone_ha, licenseidtoken, email, dmvpn_tunnel, dmvpn_key, default_user, default_password,subscription_id, api_client_id, api_client_secret, tenant_id, network_contributor_role_id, router_app_object_id, router_app_principal_id, router_app_key)
    python_modules.terraform.dmvpn_create_definition_files(vpc_template, vpc_number, cloud_provider, dmvpn_role)

    # Deploy Cloud Definitions
    python_modules.terraform.init_terraform(vpc_number)
    python_modules.terraform.apply_terraform(vpc_number)

    # Create Ansible host_vars files
    tfstate_dictionary = python_modules.ansible_hosts.main(cloud_provider, vpc_template, vpc_number, dictionary_tfvars)

    # Configure DMVPN Hub
    if dmvpn_role == "dmvpn_hub":
        with open('Ansible/hosts') as f:
            lines = f.readlines()
        newline = tfstate_dictionary["ip_a"] + "\n"
        lines.append(newline)
        print(lines)
        with open('Ansible/hosts', 'w') as f_out:
            for line in lines:
                f_out.write(line)
        python_modules.dmvpn_hub_create.main(tfstate_dictionary)
        w = subprocess.Popen(['ansible-playbook', 'create_csr1000v_hub_a.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_a"]), '-vvvv'],
                             cwd="Ansible")
        w.wait()
        w = subprocess.Popen(['ansible-playbook', 'update_dmvpn_nhs_bgp_addresses.yml', '--extra-vars', 'target=csr1000v_aws', '-vvvv'],
                             cwd="Ansible")
        w.wait()

    # Configure DMVPN Spoke
    if dmvpn_role == "dmvpn_spoke":
        with open('Ansible/hosts') as f:
            lines = f.readlines()
        newline = tfstate_dictionary["ip_a"] + "\n"
        lines.append(newline)
        if vpc_template == 'high_availability':
            newline = tfstate_dictionary["ip_b"] + "\n"
            lines.append(newline)
        print(lines)
        with open('Ansible/hosts', 'w') as f_out:
            for line in lines:
                f_out.write(line)
        if vpc_template == 'dev':
            w = subprocess.Popen(['ansible-playbook', 'create_csr1000v_spoke_a.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_a"]), '-vvvv'],
                                 cwd="Ansible")
            w.wait()
        if vpc_template == 'standard':
            w = subprocess.Popen(['ansible-playbook', 'create_csr1000v_spoke_a.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_a"]), '-vvvv'],
                                 cwd="Ansible")
            w.wait()
        if vpc_template == 'high_availability':
            if cloud_provider == 'azure':
                w = subprocess.Popen(['ansible-playbook', 'showrun.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_a"]), '-vvvv'],
                                     cwd="Ansible")
                w.wait()
                w = subprocess.Popen(['ansible-playbook', 'showrun.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_b"]), '-vvvv'],
                                     cwd="Ansible")
                w.wait()
                python_modules.azure_ha.main(vpc_number, tfstate_dictionary["ip_a"], tfstate_dictionary["ip_b"],
                                             settings_dictionary)

            w = subprocess.Popen(['ansible-playbook', 'create_csr1000v_spoke_a_ha.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_a"]), '-vvvv'],
                                 cwd="Ansible")
            w.wait()
            w = subprocess.Popen(['ansible-playbook', 'create_csr1000v_spoke_b_ha.yml', '--extra-vars', 'target={}'.format(tfstate_dictionary["ip_b"]), '-vvvv'],
                                 cwd="Ansible")
            w.wait()


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