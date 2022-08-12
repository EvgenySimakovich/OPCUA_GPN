from models import DiscreteValve, AnalogValve
from settings import *

objects = server.get_objects_node()
factory = objects.add_object(idx, "Factory")
machine = factory.add_object(idx, "Machine")

discrete_valve1 = DiscreteValve(machine, 'DiscreteValve')
analog_valve1 = AnalogValve(machine, 'AnalogValve')

print('START server')
server.start()
print('Server started')
input('Press any key to STOP server\n')
server.stop()
print('Server stoped')