from datetime import datetime
import re
import socket

# Common ports from "common-ports.py"
common_ports = dict()
fhand = open("common_ports.py", "r")
for line in fhand:
    if not ":" in line:
        continue
    line = line.strip().split(":")
    common_ports[int(line[0])] = line[1].lstrip()[1:-2]

fhand.close()

def ipv4_address_validator(address) :
    lst = address.split(".")
    for bits in lst:
        if int(bits) > 255 : return False
    return True


def get_open_ports(target, port_range, verbose=False):
    t1 = datetime.now()
    targetIsIpv4 = False
    if re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", target):
        targetIsIpv4 = True

    # Address validation
    if targetIsIpv4 :
        validIp = ipv4_address_validator(target)
        if not validIp :
            return "Error: Invalid IP address"
    else:
        try:
            socket.gethostbyname(target)
        except:
            return "Error: Invalid hostname"

    if verbose:
        # Setting hostname and Ip address to their respective value
        if targetIsIpv4:
            Ip = target
            hostname = None
            try:
                hostname = socket.gethostbyaddr(Ip)[0]
            except:
                print("The host " + Ip +" doesn't return a hostname.")
        else:
            Ip = socket.gethostbyname(target)
            hostname = target
            
        if hostname :
            open_ports = 'Open ports for ' + hostname + ' (' + Ip + ')\nPORT     SERVICE\n'
        else:
            open_ports = 'Open ports for ' + Ip + '\nPORT     SERVICE\n'

        for port in range(port_range[0], port_range[-1] + 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
            
                conn = s.connect_ex((target, port))
                if conn == 0 :
                    service = common_ports.get(port, 'Uncommon port')
                    n = 9 - len(str(port))
                    if port != port_range[-1]:
                        open_ports += str(port) + (' ' * n) + service + '\n'
                    else:
                        open_ports += str(port) + (' ' * n) + service
                s.close
            except socket.error :
                s.close()
                continue
            except:
                s.close()
                continue

    else:
        open_ports = []

        for port in range(port_range[0], port_range[-1]+1): 
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)

                conn = s.connect_ex((target, port))
                if conn == 0:
                    open_ports.append(port)
                s.close()
            except:
                continue

    
    print( "Scan completed in ", datetime.now() - t1 )
    if verbose: return open_ports[:-1]
    return open_ports


# result = get_open_ports("137.74.187.104", [440, 450], True)

# print(result)
# result = get_open_ports("104.26.10.78", [440, 450], True)
# print(result)
