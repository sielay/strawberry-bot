import daemon

from .eventloop import eventloop

with daemon.DaemonContext():
    eventloop()
