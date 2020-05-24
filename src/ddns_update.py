#!/usr/bin/python3

import logging
import requests
from requests.exceptions import RequestException
import click
from os import environ

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("ddns updater")


def response_successful(response_text):
    return response_text.startswith("good") or response_text.startswith("nochg")


@click.command()
@click.option(
    "--host",
    required=True,
    default=lambda: environ.get("DDNS_HOST", None),
    help="The dns name to update",
)
@click.option(
    "--key",
    required=True,
    default=lambda: environ.get("DDNS_KEY", None),
    help="The ddns authorization key",
)
@click.option(
    "--ip",
    required=True,
    default=lambda: environ.get("DDNS_IP", None),
    help="The hosts new ip address in ipv4 or ipv6 format",
)
def ddns_update(host, key, ip):
    url = f"https://dyndns.strato.com/nic/update?hostname={host}&myip={ip}"

    try:
        response = requests.get(url, auth=(host, key), timeout=3)
        response.raise_for_status()

        if not response_successful(response.text):
            raise RequestException("update failed")

    except RequestException as error:
        log.debug(response.text.strip())
        log.error(error)
        return

    log.debug(response.text.strip())
    log.info("update successful")


if __name__ == "__main__":
    ddns_update()
