"""
:author: Zilvinas Binisevicius <zilvinas@binis.me>
"""
import domintell
import domintell.messages
from domintell.messages.temperature_status import PBLTemperaturetatusMessage

DOM_ABSENSE = 1
DOM_AUTO = 2
DOM_COMFORT = 5
DOM_FROST = 6


class DTEM01Module(domintell.Module):
    """
    DTEM01 - temperature controll module (1 channels)    
    """
    COMMAND_CODE = 'TE1'

    def __init__(self, serial_number, controller):
        domintell.Module.__init__(self, serial_number, controller)
        self._temperature = None
        self._mode = None
        self._set_point = None
        self._range = None

    def get_range(self):
        return self._range

    def get_temperature(self):
        return self._temperature
    
    def get_mode(self):
        return self._mode
    
    def get_set_point(self):
        return self._set_point

    def set_temperature(self, temperature):
        message = domintell.SetTemperatureMessage(self.get_module_code(), self.get_serial_number(), temperature)
        self._controller.send(message)
    
    def set_mode(self, mode):
        """ Set temperature controll mode, modes:
        1 - Absense
        2 - AUTOMATIC
        5 - Comfort
        6 - Frost (if enabled in controller)
        """
        message = domintell.SetTemperatureModeMessage(self.get_module_code(), self.get_serial_number(), mode)
        self._controller.send(message) 
    
    def set_automatic(self):
        message = domintell.SetTemperatureAutomaticMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def set_absence(self):
        message = domintell.SetTemperatureAbsenceMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)
 
    def set_comfort(self):
        message = domintell.SetTemperatureComfortMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def set_frost(self):
        message = domintell.SetTemperatureFrostMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def number_of_channels(self):
        return 1

    def _on_message(self, message):
        if isinstance(message, domintell.TE1TemperaturetatusMessage):
            self._temperature = message.get_temperature()
            self._set_point = message.get_set_point()
            self._mode = self._mode_text_to_number(message.get_mode())
            print("mode", self._mode)
            self._range = message.get_range()

            for ch in range(0, self.number_of_channels()):
                if ch in self._callbacks:
                    for callback in self._callbacks[ch]:
                        callback(self._temperature, self._mode, self._set_point, self._range)

    def _mode_text_to_number(self, mode):
        if mode == 'AUTO':
            return DOM_AUTO 
        elif mode == 'ABSENCE':
            return DOM_ABSENSE
        elif mode == 'COMFORT':
            return DOM_COMFORT
        elif mode == 'FROST':
            return DOM_FROST
        return DOM_AUTO

class DTEM02Module(domintell.Module):
    """
    DTEM02 -  controll module (1 channels)    
    """
    COMMAND_CODE = 'TE2'
    def _on_message(self, message):
        if isinstance(message, domintell.TE2TemperaturetatusMessage):
            self._temperature = message.get_temperature()
            self._set_point = message.get_set_point()
            self._mode = message.get_mode()
            self._range = message.get_range()

            for ch in range(0, self.number_of_channels()):
                if ch in self._callbacks:
                    for callback in self._callbacks[ch]:
                        callback(self._temperature, self._mode, self._set_point, self._range)

class DPBLModule(domintell.Module):
    """
    PBL - LCD panel with temperature sensor
    """
    COMMAND_CODE = "PBL"

    def __init__(self, serial_number, controller):
        super().__init__(serial_number, controller)
        self._temperature = None
        self._mode = None
        self._set_point = None
        self._range = None

    def _mode_text_to_number(self, mode_text):
        mode_text = mode_text.upper()
        if mode_text == "ABSENCE":
            return 1
        elif mode_text == "AUTO":
            return 2
        elif mode_text == "COMFORT":
            return 5
        elif mode_text == "FROST":
            return 6
        elif mode_text == "HEATING" or mode_text == "COOLING":
            # Heating/Cooling are NOT Domintell modes, they are regulation states.
            # They are shown as AUTO in Home Assistant.
            return 2
        return 2  # fallback to AUTO


    def get_temperature(self):
        return self._temperature

    def get_mode(self):
        return self._mode

    def get_set_point(self):
        return self._set_point

    def get_range(self):
        return self._range

    def number_of_channels(self):
        return 1  # only temp


    def set_temperature(self, temperature):
        """Set target temperature (set point)."""
        message = domintell.SetTemperatureMessage(
            self.get_module_code(),
            self.get_serial_number(),
            temperature
        )
        self._controller.send(message)

    def set_mode(self, mode):
        """Set control mode: 1=Absense, 2=AUTO, 5=Comfort, 6=Frost"""
        message = domintell.SetTemperatureModeMessage(
            self.get_module_code(),
            self.get_serial_number(),
            mode
        )
        self._controller.send(message)

    def set_automatic(self):
        message = domintell.SetTemperatureAutomaticMessage(
            self.get_module_code(),
            self.get_serial_number()
        )
        self._controller.send(message)

    def set_absence(self):
        message = domintell.SetTemperatureAbsenceMessage(
            self.get_module_code(),
            self.get_serial_number()
        )
        self._controller.send(message)

    def set_comfort(self):
        message = domintell.SetTemperatureComfortMessage(
            self.get_module_code(),
            self.get_serial_number()
        )
        self._controller.send(message)

    def set_frost(self):
        message = domintell.SetTemperatureFrostMessage(
            self.get_module_code(),
            self.get_serial_number()
        )
        self._controller.send(message)

    def _on_message(self, message):
        if isinstance(message, PBLTemperaturetatusMessage):
            if message.dataType == "T":
                self._temperature = message.get_temperature()
                self._set_point = message.get_set_point()
                self._mode = self._mode_text_to_number(message.get_mode())
                self._range = message.get_range()

                for ch in range(self.number_of_channels()):
                    if ch in self._callbacks:
                        for callback in self._callbacks[ch]:
                            callback(
                                self._temperature,
                                self._mode,
                                self._set_point,
                                self._range,
                            )


domintell.register_module_class(DTEM01Module)
domintell.register_module_class(DTEM02Module)
domintell.register_module_class(DPBLModule)