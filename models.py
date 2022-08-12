from opcua import uamethod, ua
from abc import ABC, abstractmethod
from settings import *


class Valve(ABC):
    """
    Базовый класс для создания объекта клапан.
    При инициализации принимает два аргумента: узел модели OPC, в котором создается объект, и имя объекта.
    """
    def __init__(self, node, name):
        self._node = node
        self._name = name
        self._cteare_valve()
        self._create_valve_interface()

    def _cteare_valve(self):
        """
        Метод для создания объекта клапан в модели OPC.
        """
        self._obj = self._node.add_object(idx, self._name)
        self._valve_opened = self._obj.add_variable(idx, f'{self._name}_opened', False)
        self._valve_closed = self._obj.add_variable(idx, f'{self._name}_closed', True)

    @abstractmethod
    def _create_valve_interface(self):
        """
        Метод для создания интерфейсов управления объектом модели OPC.
        """


class DiscreteValve(Valve):
    """
    Дочерний класс для создания объекта дискретный клапан.
    Описание состояния дискретного клапана:
    _valve_opened: bool
    _valve_closed: bool
    Интерфейсы управления объектом:
    open(): func
    close(): func
    """

    def _create_valve_interface(self):
        self._obj.add_method(idx, "open", self.open)
        self._obj.add_method(idx, "close", self.close)

    @uamethod
    def open(self, parent):
        self._valve_opened.set_value(True)
        self._valve_closed.set_value(False)

    @uamethod
    def close(self, parent):
        self._valve_opened.set_value(False)
        self._valve_closed.set_value(True)


class AnalogValve(Valve):
    """
    Дочерний класс для создания объекта аналоговый клапан.
    Описание состояния аналогового клапана:
    _valve_opened: bool
    _valve_closed: bool
    _valve_state: int
    Интерфейсы управления объектом:
    open(): func
    close(): func
    """

    def _create_valve_interface(self):
        self._valve_state = self._obj.add_variable(idx, f'{self._name}_state', 0)

        in_arg_percent = ua.Argument()
        in_arg_percent.Name = "Inpunt percent"
        in_arg_percent.DataType = ua.NodeId(ua.ObjectIds.UInt32)
        in_arg_percent.ValueRank = -1
        in_arg_percent.ArrayDimensions = []
        in_arg_percent.Description = ua.LocalizedText("Percent (0 - 100)")

        self._obj.add_method(idx, "Open valve", self.open, [in_arg_percent])
        self._obj.add_method(idx, "Close valve", self.close, [in_arg_percent])

    @uamethod
    def open(self, parent, arg_percent):
        """
        Метод в качестве аргумента принимает процент открытия, на который нужно изменить
        положение задвижки клапана.
        """
        current_state = self._valve_state.get_value()
        result_state = current_state + arg_percent

        if result_state >= 100:
            result_state = 100

        if current_state == 0 and result_state > 0:
            self._valve_opened.set_value(True)
            self._valve_closed.set_value(False)

        self._valve_state.set_value(result_state)

    @uamethod
    def close(self, parent, arg_percent):
        """
        Метод в качестве аргумента принимает процент закрытия, на который нужно изменить
        положение задвижки клапана.
        """
        current_state = self._valve_state.get_value()
        result_state = current_state - arg_percent

        if result_state <= 0:
            result_state = 0
            self._valve_opened.set_value(False)
            self._valve_closed.set_value(True)

        self._valve_state.set_value(result_state)
