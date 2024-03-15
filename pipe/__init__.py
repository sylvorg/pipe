import rich.traceback as RichTraceback

RichTraceback.install(show_locals=True)

from beartype.claw import beartype_this_package

beartype_this_package()

from pipe.pipe import *
