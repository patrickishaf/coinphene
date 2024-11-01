from datetime import datetime
import logging

class Log():
    def __init__(self, **kwargs):
        self.event = kwargs["event"]
        self.message = kwargs["message"]
        self.username = kwargs["username"]
        self.user_id = kwargs["user_id"]
        self.timestamp = kwargs["timestamp"]

    def __repr__(self):
        return f"{self.timestamp}: Log(event={self.event}, message={self.message}, username={self.username}, user_id={self.user_id})"
    
    def to_string(self):
        return self.__repr__()


class LogBuilder():

    def __init__(self):
        self.event = None
        self.message = None
        self.username = None
        self.user_id = None
        self.timestamp = None

    def set_event(self, event: str):
        self.event = event
        return self

    def set_message(self, message: str):
        self.message = message
        return self

    def set_username(self, username):
        self.username = username
        return self

    def set_userid(self, user_id):
        self.user_id = user_id
        return self

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self
    
    def build(self):
        if self.event is None:
            raise LogBuildingException("event not initialized")
        elif self.message is None:
            raise LogBuildingException("message not initialized")
        elif self.timestamp is None:
            self.timestamp = f"{datetime.now()}"
        
        self.log = Log(event=self.event, message=self.message, username=self.username, user_id=self.user_id, timestamp=self.timestamp)
        return self.log

    
class LogBuildingException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = args[0]

    def __repr__(self):
        return f"LogBuildingException({self.message})"
    

class AppLogger(logging.Logger):
    def __init__(self, name, level = logging.INFO):
        super().__init__(name, level)
    

def init_file_logging():
    logging.basicConfig(
        filename="logs.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.setLoggerClass(AppLogger)
    logging.getLogger("sqlalchemy.engine").disabled = True
