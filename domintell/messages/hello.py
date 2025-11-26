
import domintell


class Hello(domintell.Command):
    """
        send: &Hello message
    """
    def __init__(self):
        domintell.Command.__init__(self)

    def command(self):
        return "&HELLO"
