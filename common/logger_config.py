import os
import logging


def logger_config(logger_name, log_folder, log_file_name):
    log_path = os.path.join(logger_name, log_folder, log_file_name)
    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(logger_name)
