#!/usr/bin/python3

from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("ddns updater")

if __name__ == "__main__":
    log.info("starting...")
    sequence = 1
    while True:
        log.debug(f"update sequence {sequence}")
        sequence += 1
        sleep(5)
