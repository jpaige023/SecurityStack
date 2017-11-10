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
