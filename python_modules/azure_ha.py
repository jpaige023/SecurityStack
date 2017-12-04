import simplejson as json
import time
import requests
import random
import paramiko



def main(vpc_number, ip_a, ip_b, settings_dictionary):
    # bearer_token_get
    url = 'https://login.microsoftonline.com/{}/oauth2/token'.format(settings_dictionary['tenant_id'])
    data = {'grant_type': 'client_credentials', 'client_id': settings_dictionary['api_client_id'], 'client_secret': settings_dictionary['api_client_secret'], 'resource': 'https://management.azure.com/'}
    r = requests.post(url, data=data)
    body = r.json()
    print body
    bearer_token = body['access_token']

    # azure_route_table_access_control_add
    random_id_1 = random.randrange(10000000, 100000000)
    random_id_2 = random.randrange(100000000000, 1000000000000)
    url = 'https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/routeTables/RTPrivate/providers/Microsoft.Authorization/roleAssignments/{}-1234-5665-4321-{}?api-version=2015-07-01'.format(
        settings_dictionary['subscription_id'], vpc_number, random_id_1, random_id_2)
    headers = {'Authorization': 'Bearer {}'.format(bearer_token), 'Content-Type': 'application/json'}
    data = {"properties": {
        "roleDefinitionId": "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/routeTables/RTPrivate/providers/Microsoft.Authorization/roleDefinitions/{}".format(
            settings_dictionary['subscription_id'], vpc_number, settings_dictionary['network_contributor_role_id']), "principalId": "{}".format(settings_dictionary['router_app_principal_id'])}}
    r = requests.put(url, headers=headers, data=json.dumps(data))
    body = r.json()
    print "Private Route Table access control update complete!"


    # azure_create_trustpoint
    """ needs paramiko and time"""
    username = settings_dictionary['default_user']
    password = settings_dictionary['default_password']
    ip_list = [ip_a, ip_b]

    for ip in ip_list:
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(hostname=ip, port=22, username=username, password=password, look_for_keys=False,
                            allow_agent=False)

        remote_conn = remote_conn_pre.invoke_shell()
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('conf t\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('crypto pki trustpool import url http://www.cisco.com/security/pki/trs/ios.p7b\n')
        time.sleep(20)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('crypto pki trustpoint MicrosoftSSL\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('enrollment terminal\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('subject-name cn=msit_tls_ca.crt\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('vrf internet-vrf\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('exit\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('crypto pki authenticate MicrosoftSSL\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output
        # This is microsoft's current crt in pem format from https://www.microsoft.com/pki/mscorp/cps/default.htm
        remote_conn.send('MIIFtDCCBJygAwIBAgIQDywQyVsGwJN/uNRJ+D6FaTANBgkqhkiG9w0BAQsFADBa\n')
        time.sleep(.5)
        remote_conn.send('MQswCQYDVQQGEwJJRTESMBAGA1UEChMJQmFsdGltb3JlMRMwEQYDVQQLEwpDeWJl\n')
        time.sleep(.5)
        remote_conn.send('clRydXN0MSIwIAYDVQQDExlCYWx0aW1vcmUgQ3liZXJUcnVzdCBSb290MB4XDTE2\n')
        time.sleep(.5)
        remote_conn.send('MDUyMDEyNTE1N1oXDTI0MDUyMDEyNTE1N1owgYsxCzAJBgNVBAYTAlVTMRMwEQYD\n')
        time.sleep(.5)
        remote_conn.send('VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy\n')
        time.sleep(.5)
        remote_conn.send('b3NvZnQgQ29ycG9yYXRpb24xFTATBgNVBAsTDE1pY3Jvc29mdCBJVDEeMBwGA1UE\n')
        time.sleep(.5)
        remote_conn.send('AxMVTWljcm9zb2Z0IElUIFRMUyBDQSAyMIICIjANBgkqhkiG9w0BAQEFAAOCAg8A\n')
        time.sleep(.5)
        remote_conn.send('MIICCgKCAgEAnqoVwRuhY1/mURjFFrsR3AtNm5EKukBJK9zWBgvFd1ksNEJFC06o\n')
        time.sleep(.5)
        remote_conn.send('yRbwKPMflpW/HtOfzIeBliGk57MwZq18bgASr70sPUWuoD917HUgBfxBYoF8zA7Z\n')
        time.sleep(.5)
        remote_conn.send('Ie5zAHODFboJL7Fg/apgbQs/GiZZNCi0QkQUWzw0nTUmVSNQ0mz6pCu95Dv1WMsL\n')
        time.sleep(.5)
        remote_conn.send('GyPGfdN9zD3Q/QEDyJ695QgjRIxYA1DUE+54ti2k6r0ycKFQYkyWwZ25HD1h2kYt\n')
        time.sleep(.5)
        remote_conn.send('3ovW85vF6y7tjTqUEcLbgKUCB81/955hdLLsbFd6f9o2PkU8xuOc3U+bUedvv6Sb\n')
        time.sleep(.5)
        remote_conn.send('tvGjBEZeFyH8/CaQhzlsKMH0+OPOFv/bMqcLarPw1V1sOV1bl4W9vi2278niblzI\n')
        time.sleep(.5)
        remote_conn.send('bEHt7nN888p4KNIwqCcXaGhbtS4tjn3NKI6v1d2XRyxIvCJDjgoZ09zF39Pyoe92\n')
        time.sleep(.5)
        remote_conn.send('sSRikZh7xns4tQEQ8BCs4o5NBSx8UxEsgyzNSskWGEWqsIjt+7+A1skDDZv6k2o8\n')
        time.sleep(.5)
        remote_conn.send('VCHNbTLFKS7d72wMI4ErpzVsBIicxaG2ezuMBBuqThxIiJ+G9zfoP9lxim/9rvJA\n')
        time.sleep(.5)
        remote_conn.send('xbh3nujA1VJfkOYTJIojEAYCxR3QjEoGdapJmBle97AfqEBnwoJsu2wav8h9v+po\n')
        time.sleep(.5)
        remote_conn.send('DL4h6dRzRUxY1DHypcFlXGoHu/REQgFLq2IN30/AhQLN90Pj9TT2RQECAwEAAaOC\n')
        time.sleep(.5)
        remote_conn.send('AUIwggE+MB0GA1UdDgQWBBSRnjtEbD1XnEJ3KjTXT9HMSpcs2jAfBgNVHSMEGDAW\n')
        time.sleep(.5)
        remote_conn.send('gBTlnVkwgkdYzKz6CFQ2hns6tQRN8DASBgNVHRMBAf8ECDAGAQH/AgEAMA4GA1Ud\n')
        time.sleep(.5)
        remote_conn.send('DwEB/wQEAwIBhjAnBgNVHSUEIDAeBggrBgEFBQcDAQYIKwYBBQUHAwIGCCsGAQUF\n')
        time.sleep(.5)
        remote_conn.send('BwMJMDQGCCsGAQUFBwEBBCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGln\n')
        time.sleep(.5)
        remote_conn.send('aWNlcnQuY29tMDoGA1UdHwQzMDEwL6AtoCuGKWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0\n')
        time.sleep(.5)
        remote_conn.send('LmNvbS9PbW5pcm9vdDIwMjUuY3JsMD0GA1UdIAQ2MDQwMgYEVR0gADAqMCgGCCsG\n')
        time.sleep(.5)
        remote_conn.send('AQUFBwIBFhxodHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BTMA0GCSqGSIb3DQEB\n')
        time.sleep(.5)
        remote_conn.send('CwUAA4IBAQBsf+pqb89rW8E0rP/cDuB9ixMX4C9OWQ7EA7n0BSllR64ZmuhU9mTV\n')
        time.sleep(.5)
        remote_conn.send('2L0G4HEiGXvOmt15i99wJ0ho2/dvMxm1ZeufkAfMuEc5fQ9RE5ENgNR2UCuFB2Bt\n')
        time.sleep(.5)
        remote_conn.send('bVmaKUAWxscN4GpXS4AJv+/HS0VXs5Su19J0DA8Bg+lo8ekCl4dq2G1m1WsCvFBI\n')
        time.sleep(.5)
        remote_conn.send('oLIjd4neCLlGoxT2jA43lj2JpQ/SMkLkLy9DXj/JHdsqJDR5ogcij4VIX8V+bVD0\n')
        time.sleep(.5)
        remote_conn.send('NCw7kQa6Ulq9Zo0jDEq1at4zSeH4mV2PMM3LwIXBA2xo5sda1cnUWJo3Pq4uMgcL\n')
        time.sleep(.5)
        remote_conn.send('e0t+fCut38NMkTl8F0arflspaqUVVUov\n\n')
        time.sleep(.5)
        remote_conn.send('quit\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('yes\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output

        remote_conn.send('end\n')
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print output


if __name__ == "__main__":
    main()