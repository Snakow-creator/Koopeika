import logging

from secret.config import DEBUG

log = logging.getLogger(__name__)

console = logging.StreamHandler()
file_handler = logging.FileHandler("logs.log")

def start_logging():
    if DEBUG == True: # developer mode
        log.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)

    else:
        log.setLevel(logging.INFO)
        console.setLevel(logging.INFO)

    formatter = logging.Formatter("%(name)-4s: %(levelname)-8s %(message)s %(asctime)s")
    console.setFormatter(formatter)

    formatter = logging.Formatter(
        "[%(asctime)s]\t Filename: %(module)s(%(lineno)d line) - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    if not log.hasHandlers():
        log.addHandler(console)
        log.addHandler(file_handler)

    log.info("Launched")
