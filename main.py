import simplejson as json
import re
import python_modules.vdss_ip_generation

def main():
    cidr_block = "10.0.0.0/21"
    region = "us-west-1"
    availability_zone = "us-west-1a"
    python_modules.vdss_ip_generation.main(cidr_block, region, availability_zone)



if __name__ == "__main__":
    main()