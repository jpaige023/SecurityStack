from unittest import TestCase
from vdss_ip_generation import vdss_subnets_generation


class TestSubnet_generation(TestCase):
    def test_vdss_subnets_generation(self):
        r = vdss_subnets_generation("172.31.0.0/21")
        self.assertEqual(r, ({'subnet_public': '172.31.0.0/24', 'subnet_management': '172.31.1.0/24', 'subnet_asav_ftd': '172.31.2.0/24', 'subnet_outside_csr_fw': '172.31.4.0/23', 'subnet_inside_csr_fw': '172.31.6.0/23'}))
