import xml.etree.ElementTree as ET
from opcua import Server


configFilePath = 'config.xml'
root = ET.parse(configFilePath).getroot()

serverElement = root.find('server')
server_name = serverElement.attrib.get('name')
ip = serverElement.find('ip').text
port = serverElement.find('port').text
domain = serverElement.find('domain').text

fullIpAddress = f"opc.tcp://{ip}:{port}"
uri = f"http://{domain}"

server = Server()
server.set_endpoint(fullIpAddress)
server.set_server_name(server_name)
idx = server.register_namespace(uri)