import domintell

class TimeoutDisable(domintell.Command):
    """
        send: TIMEOUT=0 to disable session timeout
    """
    def __init__(self):
        super().__init__()

    def command(self):
        return "TIMEOUT=0"
