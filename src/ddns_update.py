#!/usr/bin/python3

import logging
import requests
from requests.exceptions import RequestException
import click
from os import environ
from netifaces import interfaces, ifaddresses, AF_INET6
from ipaddress import ip_address
from time import sleep
import socket

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s - %(name)s %(levelname)-8s: %(message)s")
log = logging.getLogger("ddns updater")


def get_global_address(address_family):
    for interface in interfaces():
        if_addresses = ifaddresses(interface)
        if address_family in if_addresses:
            for address in if_addresses[address_family]:
                addr = ip_address(address["addr"].split("%")[0])
                if addr.is_global:
                    return addr
    return None


def get_global_ipv6():
    return get_global_address(AF_INET6)


def response_successful(response_text):
    return response_text.startswith("good") or response_text.startswith("nochg")


def ddns_update(host, key, ip):
    url = f"https://dyndns.strato.com/nic/update?hostname={host}&myip={ip}"

    try:
        response = requests.get(url, auth=(host, key), timeout=3)
    except RequestException as error:
        log.error(error)
        return False

    try:
        response.raise_for_status()

        if not response_successful(response.text):
            raise RequestException("update failed")

    except RequestException as error:
        log.error(response.text.strip())
        log.error(error)
        return False

    log.debug(response.text.strip())
    log.info("update successful")

    return True


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
def loop_ddns_update(host, key):
    last_ip = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
    log.debug(f"current registered address: {last_ip}")

    while True:
        current_ip = get_global_ipv6()
        if current_ip != last_ip:
            if ddns_update(host, key, current_ip):
                last_ip = current_ip
        else:
            log.debug("skipped update, ip address unchanged")
        sleep(30)


if __name__ == "__main__":
    log.info("starting...")
    loop_ddns_update()
