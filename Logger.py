import logging
import sys
import io
import time

class Logger:

    def __init__(self,
                 log_name):
        self.format = f'[%(asctime)s] | [%(levelname)s] | [%(name)s] | [%(threadName)s] | [%(pathname)s] | : | [%(message)s]'
        self.formater = logging.Formatter(self.format)
        self.log_name = log_name
        logging.basicConfig(format=self.format)
        self.log = logging.getLogger(self.log_name)
        self.log.setLevel(logging.DEBUG)
        self.log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.log_capture_string)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formater)
        self.log.addHandler(ch)


    def get_logs(self,log):
        log_content = log.split('|')
        log_date = log_content[0].strip()
        log_type = log_content[1].strip()
        log_name = log_content[2].strip()
        log_thread = log_content[3].strip()
        log_issued_path = log_content[4].strip()
        log_message = log_content[-1].strip()

        return log_date,log_type,log_name,log_thread,log_issued_path,log_message