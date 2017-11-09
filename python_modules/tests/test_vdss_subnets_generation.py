from unittest import TestCase
from vdss_ip_generation import vpc_cidr_networkid_netmask_generation

class TestVdss_subnets_generation(TestCase):
    def test_vpc_cidr_networkid_netmask_generation(self):
        r = vpc_cidr_networkid_netmask_generation("172.31.0.0/21")
        self.assertEqual(r, ({'vpc_cidr_block_network_ID': '172.31.0.0', 'vpc_cidr_block_netmask': '255.255.248.0'}))
