import subprocess
from subprocess import Popen, PIPE
import shlex


def init_terraform(vpc_number):
    # import subprocess
    # import os
    # from subprocess import Popen, PIPE
    # import shlex
    # import sys
    # vpc_number = "17"

    exitcode = 1
    while exitcode != 0:
        print "\n\nInitializing Terraform Provider"
        cmd = "terraform init"
        args = shlex.split(cmd)
        proc = Popen(args, stdout=PIPE, stderr=PIPE, cwd="VPCs/{}".format(vpc_number))
        out, err = proc.communicate()
        print out
        print err
        exitcode = proc.returncode
    return


def apply_terraform(vpc_number):
    exitcode = 1
    while exitcode != 0:
        print "\n\nApplying Terraform cloud Definition. This can take a few minutes..."
        cmd = "terraform apply -auto-approve=true"
        args = shlex.split(cmd)
        proc = Popen(args, stdout=PIPE, stderr=PIPE, cwd="VPCs/{}".format(vpc_number))
        out, err = proc.communicate()
        print out
        print err
        exitcode = proc.returncode
    return


def terraform_tfvars_createfile(cloud_provider, vpc_number, settings_dictionary, cloud_provider_region=None):
    if cloud_provider == 'aws':
        aws_access_key = settings_dictionary['keys']['cloud'][cloud_provider][cloud_provider_region]['aws_access_key']
        aws_secret_key = settings_dictionary['keys']['cloud'][cloud_provider][cloud_provider_region]['aws_secret_key']
        aws_key_name = settings_dictionary['keys']['cloud'][cloud_provider][cloud_provider_region]['aws_key_name']
        aws_tfvars_template = ['aws_access_key = "{}"\r\n'.format(aws_access_key),
                               'aws_secret_key = "{}"\r\n'.format(aws_secret_key),
                               'aws_key_name = "{}"'.format(aws_key_name)]
        g = open("VPCs/{}/terraform.tfvars".format(vpc_number), "w")
        for line in aws_tfvars_template:
            g.write(line)
        g.close()

    if cloud_provider == 'azure':
        subscription_id = settings_dictionary['keys']['cloud'][cloud_provider]['subscription_id']
        client_id = settings_dictionary['keys']['cloud'][cloud_provider]['client_id']
        client_secret = settings_dictionary['keys']['cloud'][cloud_provider]['client_secret']
        tenant_id = settings_dictionary['keys']['cloud'][cloud_provider]['tenant_id']
        default_user = settings_dictionary['keys']['cloud'][cloud_provider]['default_user']
        default_password= settings_dictionary['keys']['cloud'][cloud_provider]['default_password']
        azure_tfvars_template = ['subscription_id = "{}"\n'.format(subscription_id),
                                 'client_id = "{}"\n'.format(client_id),
                                 'client_secret = "{}"\n'.format(client_secret),
                                 'tenant_id = "{}"\n'.format(tenant_id), 'default_user = "{}"\n'.format(default_user),
                                 'default_password = "{}"\n'.format(default_password)]
        g = open("VPCs/{}/terraform.tfvars".format(vpc_number), "w")
        for line in azure_tfvars_template:
            g.write(line)
        g.close()


def vdss_create_definition_files(vpc_number, cloud_provider='aws', device_number_csr1000v_inside_ingress_count=1,
                                     device_number_csr1000v_inside_egress_count=1,
                                     device_number_csr1000v_outside_ingress_count=1,
                                     device_number_csr1000v_outside_egress_count=1, device_number_firewalls_count=1):
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
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/vpc_security_stack/fmc_0.tf VPCs/{}".format(cloud_provider.upper(), vpc_number),
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

def dmvpn_create_definition_files(vpc_template, vpc_number, cloud_provider, dmvpn_role):
    # copy terraform modules
    subprocess.call(
        "cp TEMPLATES/Cloud/{}/{}/{}/* VPCs/{}".format(cloud_provider.upper(), dmvpn_role, vpc_template, vpc_number),
        shell=True)

