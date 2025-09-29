from queue import Queue, Full
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from QueueData import QueueData
import logging
import threading
import socket


class OSCReceiver:
    """Non-blocking OSC receiver that pushes parsed messages into a queue.

    - Runs the OSC UDP server on a dedicated thread (won't block your main/control loop).
    - Applies gentle backpressure: when the queue is full, drop the oldest item to keep latency low.
    - Minimal work on the hot path (no per-arg debug spam, no redundant path checks).
    """

    def add_value_to_queue(self, key, value):
        """Non-blocking enqueue with gentle backpressure: drop oldest, keep newest."""
        data = {key: value}
        try:
            self.oscqueue.put_nowait(data)
        except Full:
            # Drop oldest item to prefer the most recent command under load
            try:
                _ = self.oscqueue.get_nowait()
            except Exception:
                pass
            try:
                self.oscqueue.put_nowait(data)
            except Exception:
                # Still full? Drop silently (never block the control loop)
                pass

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Queued %s", data)

    # ---- Handlers (dispatcher maps exact address → handler) ----

    def handleServoPose(self, address, *args):
        # Guard against NILs from some senders
        if any(v is None for v in args):
            return
        self.add_value_to_queue(key=QueueData.SERVOPOSE, value=args)

    def handleMoveJoints(self, address, *args):
        if any(v is None for v in args):
            return
        self.add_value_to_queue(key=QueueData.MOVEJOINTS, value=args)

    def handleStop(self, address, *args):
        self.add_value_to_queue(key=QueueData.STOP, value=True)

    def handleTeachMode(self, address, *args):
        self.add_value_to_queue(key=QueueData.TEACHMODE, value=True)

    def handleServoJoints(self, address, *args):
        if any(v is None for v in args):
            return
        self.add_value_to_queue(key=QueueData.SERVOJOINTS, value=args)

    # ---- Server lifecycle ----

    def _run(self):
        try:
            self.server.serve_forever()
        except OSError as e:
            logging.error("OSC server stopped: %s", e)

    def __init__(self, oscqueue: Queue, ip: str = "127.0.0.1", port: int = 10001) -> None:
        self.oscqueue = oscqueue
        self.ip = ip
        self.port = port
        self._thread = None

        dispatcher = Dispatcher()
        dispatcher.map("/servopose", self.handleServoPose)
        dispatcher.map("/movejoints", self.handleMoveJoints)
        dispatcher.map("/stop", self.handleStop)
        dispatcher.map("/teachmode", self.handleTeachMode)
        dispatcher.map("/servojoints", self.handleServoJoints)

        # Threaded server so we don't block the main/control loop
        self.server = ThreadingOSCUDPServer((self.ip, self.port), dispatcher)

        # Faster restarts on some OSes
        try:
            self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception:
            pass

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(
            target=self._run, name=f"osc@{self.ip}:{self.port}", daemon=True
        )
        self._thread.start()
        logging.info("OSC listening on %s:%d", self.ip, self.port)

    def stop(self):
        try:
            self.server.shutdown()
            self.server.server_close()
        except Exception:
            pass
        if self._thread:
            self._thread.join(timeout=1.0)
