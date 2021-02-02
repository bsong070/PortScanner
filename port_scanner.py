from common_ports import ports_and_services
import re
import socket

def get_open_ports(target, port_range, Verbose = False):
    open_ports = []
    socket.setdefaulttimeout(.15)
    ip_regex = "\d+.\d+.\d+.\d+"
    try:
      if re.search(ip_regex, target):
        ip_address = target
        try:
          url = socket.gethostbyaddr(target)[0]
        except:
          url = False
      else:
        ip_address = socket.gethostbyname(target)
        url = target

      for port in range(port_range[0], port_range[1] + 1):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if a_socket.connect_ex((target, port)) == 0:
          open_ports.append(port)
        a_socket.close()

      if Verbose == True:
        message = 'Open ports for '
        message += f'{url} ({ip_address})\n' if url else f'{ip_address}\n'
        message += 'PORT     SERVICE\n'
        for port in open_ports:
            port_str = str(port).ljust(4)
            service = ports_and_services[port]
            message += (f'{port_str}     {service}')
            if port != open_ports[-1]:
              message += '\n'
        return message
      else:
        return(open_ports)

    except:
      if re.search(ip_regex, target):
        return 'Error: Invalid IP address'
      else:
        return 'Error: Invalid hostname'
