import simplejson as json
import re

def main():

    csr1000v_inside_ingress = ["[csr1000v_inside_ingress]\n"]
    csr1000v_inside_egress = ["[csr1000v_inside_egress]\n"]
    csr1000v_outside_ingress = ["[csr1000v_outside_ingress]\n"]
    csr1000v_outside_egress = ["[csr1000v_outside_egress]\n"]
    asav_general = ["[asav_general]\n"]
    ftd_general = ["[ftd_general]\n"]
    master_list = []
    with open('vdss_ip_addresses.auto.tfvars') as json_data:
        vdss_ip_addresses = json.load(json_data)
    for key, value in vdss_ip_addresses.items():
        if re.search(r"^csr1000v_inside_ingress", key):
            if re.search(r"e2$", key):
                csr1000v_inside_ingress.append(value)
                csr1000v_inside_ingress.append("\n")
        elif re.search(r"^csr1000v_inside_egress", key):
            if re.search(r"e2$", key):
                csr1000v_inside_egress.append(value)
                csr1000v_inside_egress.append("\n")
        elif re.search(r"^csr1000v_outside_ingress", key):
            if re.search(r"e2$", key):
                csr1000v_outside_ingress.append(value)
                csr1000v_outside_ingress.append("\n")
        elif re.search(r"^csr1000v_outside_egress", key):
            if re.search(r"e2$", key):
                csr1000v_outside_egress.append(value)
                csr1000v_outside_egress.append("\n")
        elif re.search(r"^asav_general", key):
            if re.search(r"e0$", key):
                asav_general.append(value)
                asav_general.append("\n")
        elif re.search(r"^ftd_general", key):
            if re.search(r"e0$", key):
                ftd_general.append(value)
                ftd_general.append("\n")
        else:
            pass
    master_list.extend(csr1000v_inside_ingress)
    master_list.append("\n")
    master_list.extend(csr1000v_inside_egress)
    master_list.append("\n")
    master_list.extend(csr1000v_outside_ingress)
    master_list.append("\n")
    master_list.extend(csr1000v_outside_egress)
    master_list.append("\n")
    master_list.extend(asav_general)
    master_list.append("\n")
    master_list.extend(ftd_general)

    print(master_list)

    f = open("hosts", "w")
    for line in master_list:
        f.write(line)
    f.close()


if __name__ == "__main__":
   main()