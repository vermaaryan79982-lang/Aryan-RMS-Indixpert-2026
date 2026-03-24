import datetime

class ErrorHandler:

    def __init__(self):
        self.file = "error.log"

    def log(self, error_msg):
     with open(self.file, "a") as f:
                f.write(f"[{datetime.datetime.now()}] {error_msg}\n")
         