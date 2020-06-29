#### Welcome to VLSM in Python ! ####

# 1. Get the network address and the netmask
# 2. Get the number of machines expected on each subnetwork
#       (nb IP = nb machines + 2)
# 3. Sort the subnetworks by their size
# 4. Compute the number of bits needed for each subnetwork
# 5. Compute the netmask for each subnetwork
# 6. Compute each subnetwork's address
# 7. Check if the last subnetwork is actually in the original network
# 8. Print the result




import math




# check if the ip (e.g. "192.168.0.0") is a valid ip address
def is_valid_ip(ip_str: str) -> bool:
    ip_list = []
    try:
        ip_list = list(map(int, ip_str.split('.')))
    except:
        return False

    if len(ip_list) != 4:
        return False

    for i in ip_list:
        if i not in range(0,256):
            return False

    return True

# check if the netmask (e.g. "255.255.128.0") is a valid netmask
def is_valid_netmask(netmask_str: str) -> bool:
    netmask_list = []
    try:
        netmask_list = list(map(int, netmask_str.split('.')))
    except:
        return False

    if not is_valid_ip(netmask_str):
        return False

    # skip the 255
    i = 0
    while i < 4:
        if netmask_list[i] != 255:
            break
        i += 1
    
    if i < 4 and netmask_list[i] not in [0, 128, 192, 224, 240, 248, 252, 254, 255]:
        return False
    i += 1

    while i < 4:
        if netmask_list[i] != 0:
            return False
        i += 1

    return True

# converts a list (e.g. [255, 255, 128, 0]) into a number (e.g. 17)
def convert_netmask_str_to_int(netmask_str: str) -> int:
    netmask_list = list(map(int, netmask_str.split('.')))

    i = 0
    while i < 3 and netmask_list[i] == 255:
        i += 1

    if netmask_list[i] == 0:
        return i * 8
    else:
        return int(i * 8 + 8 - math.log2(256 - netmask_list[i]))

# converts an int (e.g. 17) into a list (e.g. [255, 255, 128, 0])
def convert_netmask_int_to_list(netmask_int: int) -> list:
    netmask_list = [255] * math.floor(netmask_int / 8)

    if (netmask_int % 8) != 0:
        netmask_list += [256 - 2**(8 - netmask_int % 8)]

    return netmask_list + [0] * (4 - len(netmask_list))

# converts a list (e.g. [255, 255, 128, 0]) into a string (e.g. "255.255.128.0")
def convert_ip_list_to_str(netmask_list: list) -> str:
    netmask_str = ""
    for i in netmask_list:
        netmask_str += str(i) + "."

    netmask_str = netmask_str[:-1]

    return netmask_str

# get the maximum number of machines on a network with the given netmask
def get_nb_machines_max(netmask_int: int) -> int:
    exp = 32 - netmask_int

    return max(0, 2**exp - 2)

# convert the ip (e.g. "0.0.255.255") to a number (e.g. 65535)
def convert_network_str_to_int(network_str: str) -> int:
    network_list = list(map(int, network_str.split('.')))
    network_list.reverse()
    network_int = 0

    for i in range(0, 4):
        network_int += network_list[i] * 2**(8*i)

    return network_int

# convert a number representing an ip address (e.g. 65535) to a string (e.g. "0.0.255.255")
def convert_network_int_to_str(network_int: int) -> list:
    network_list = []

    for i in range(0, 4):
        network_list.insert(0, int(network_int / 2**(8*i)) % 256)

    return convert_ip_list_to_str(network_list)

# returns the ip of the network from the ip of a machine/subnetwork and the netmask
def get_network_from_ip(ip_str: str, netmask_str: str) -> str:
    ip_int = convert_network_str_to_int(ip_str)
    netmask_int = convert_netmask_str_to_int(netmask_str)

    return convert_network_int_to_str( ip_int - (ip_int % 2**(32 - netmask_int)) )




def get_network_adress_and_netmask() -> (str, str):
    network_str = ""
    is_valid = False
    while not is_valid:
        network_str = input("please enter the network address (x.x.x.x): ")
        is_valid = is_valid_ip(network_str)

    netmask_str = ""
    is_valid = False
    while not is_valid:
        netmask_str = input("please enter the network's mask (x.x.x.x): ")
        is_valid = is_valid_netmask(netmask_str)

    return network_str, netmask_str

def get_machines_on_subnetworks(netmask_int: int) -> list:
    nb_machines_max = get_nb_machines_max(netmask_int)
    machines = []

    message = ""
    while True:
        print("-----------------------------------------------------------")
        print("| write 'stop' if you have already given every subnetwork |")
        print("-----------------------------------------------------------")
        print("already given:", machines)

        message = input("please give the number of machines on the subnetwork : ")

        if message == "stop":
            break

        try:
            nb_machines = int(message)
        except:
            continue

        if nb_machines not in range(2, nb_machines_max + 1):
            print("-> invalid number of machines")
            continue

        nb_ip = sum(machines) + nb_machines + 2 * (len(machines) + 1)
        nb_ip_max = nb_machines_max + 2
        if nb_ip > nb_ip_max:
            print("-> the number of ip needed exceeds the number of ip available")
            continue
        
        machines.append(nb_machines)

    return machines

def get_nb_bits_needed(nb_machines: int) -> int:
    return math.ceil(math.log2(nb_machines + 2))

def get_netmask_str_from_network_size(nb_bits: int) -> str:
    netmask_int = 32 - nb_bits

    netmask_list = convert_netmask_int_to_list(netmask_int)

    return convert_ip_list_to_str(netmask_list)

def compute_vlsm(network_str: str, nb_bits: list) -> list:
    subnet_addresses = [convert_network_str_to_int(network_str)]

    for i in range(0, len(machines) - 1):
        subnet_addresses.append( subnet_addresses[i] + 2**nb_bits[i] )

    return list(map(convert_network_int_to_str, subnet_addresses))




# 1. Get the network address and the netmask
network_str, netmask_str = get_network_adress_and_netmask()
print("------------" + "-" * len(network_str) + "--------------" + "-" * len(netmask_str))
print("| network :", network_str, "| netmask :", netmask_str + "|")
print("------------" + "-" * len(network_str) + "--------------" + "-" * len(netmask_str))


# 2. Get the number of machines expected on each subnetwork
netmask_int = convert_netmask_str_to_int(netmask_str)
machines = get_machines_on_subnetworks(netmask_int)
print("----------------------------------------")
print("number of machines on each subnetwork :", machines)
print("----------------------------------------")


# 3. Sort the subnetworks by their size
machines.sort(reverse=True)


# 4. Compute the number of bits needed for each subnetwork
nb_bits = list(map(get_nb_bits_needed, machines))


# 5. Compute the netmask for each subnetwork
subnetworks_netmasks = list(map(get_netmask_str_from_network_size, nb_bits))


# 6. Compute each subnetwork's address
subnet_addresses = compute_vlsm(network_str, nb_bits)


# 7. Check if the last subnetwork is actually in the original network
if get_network_from_ip(subnet_addresses[-1], netmask_str) != network_str:
    raise Exception("The given network is not big enough to")

# 8. Print the result
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")

print("network :", network_str, "netmask :", netmask_str)
print("machines :", machines)
print("nb_bits :", nb_bits)
print("subnetworks_netmasks :", subnetworks_netmasks)
print("subnet_addresses :", subnet_addresses)

