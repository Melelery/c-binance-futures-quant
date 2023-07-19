import threading
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from binance_f.impl.websocketconnection import ConnectionState
from binance_f.impl.utils.timeservice import get_current_timestamp


def watch_dog_job(*args):
    watch_dog_instance = args[0]
    for connection in watch_dog_instance.connection_list:
        if connection.state == ConnectionState.CONNECTED:
            if watch_dog_instance.is_auto_connect:
                ts = get_current_timestamp() - connection.last_receive_time
                if ts > watch_dog_instance.receive_limit_ms:
                    watch_dog_instance.logger.warning("[Sub][" + str(connection.id) + "] No response from server")
                    connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
        elif connection.in_delay_connection():
            watch_dog_instance.logger.warning("[Sub] call re_connect")
            connection.re_connect()
            pass
        elif connection.state == ConnectionState.CLOSED_ON_ERROR:
            if watch_dog_instance.is_auto_connect:
                connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
                pass


class WebSocketWatchDog(threading.Thread):
    mutex = threading.Lock()
    connection_list = list()

    def __init__(self, is_auto_connect=True, receive_limit_ms=60000, connection_delay_failure=15):
        threading.Thread.__init__(self)
        self.is_auto_connect = is_auto_connect
        self.receive_limit_ms = receive_limit_ms
        self.connection_delay_failure = connection_delay_failure
        self.logger = logging.getLogger("binance-client")
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(watch_dog_job, "interval", max_instances=10, seconds=1, args=[self])
        self.start()

    def run(self):
        self.scheduler.start()

    def on_connection_created(self, connection):
        self.mutex.acquire()
        self.connection_list.append(connection)
        self.mutex.release()

    def on_connection_closed(self, connection):
        self.mutex.acquire()
        self.connection_list.remove(connection)
        self.mutex.release()
