import socket

socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketObj.settimeout(3)

common_ports = dict()

fhand = open("common_ports.py", "r")
for line in fhand:
    if not ":" in line:
        continue
    line = line.strip().split(":")
    common_ports[int(line[0])] = line[1].lstrip()[:-1]

# print(common_ports)
# for key, value in common_ports.items():
#     print(key, value, sep=": ")


def get_open_ports(target, port_range, verbose=False):
    arr = target.split(".")

    # Address validation
    if len(target.split(".")) != 4 :
        try:
            socket.gethostbyname(target)
        except:
            return "Error: Invalid IP address"
        Ip = socket.gethostbyname(target)    
    else:
        try:
            socket.gethostbyaddr(target)
        except:
            return "Error: Invalid hostname"
        hostname = socket.gethostbyaddr(target)

    open_ports = []

    for port in port_range:
        if socketObj.connect_ex((target, port)):
            if verbose:
                # Get the service name
                service = common_ports[port]

                # In verbose mode: appending the right string to the open_ports list
                open_ports.append("Open ports for " + hostname + " " + Ip + "\nPORT     SERVICE" + port + "   " + service )
            
            else: open_ports.append(port)

    return(open_ports)


result = get_open_ports("www.google.com", [20, 400])
print(result)
