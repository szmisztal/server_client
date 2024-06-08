import os
import logging


def logger_config(logger_name, log_folder, log_file_name):
    """
    Configures and returns a logger with specified settings.

    Parameters:
    ----------
    logger_name : str
        The name of the logger.
    log_folder : str
        The folder where the log file will be stored.
    log_file_name : str
        The name of the log file.

    Returns:
    -------
    logging.Logger
        Configured logger instance.
    """
    log_path = os.path.join(logger_name, log_folder, log_file_name)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(logger_name)
