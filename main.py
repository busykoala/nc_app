from typing import Optional
import socket
import re

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()


def is_almost_ipv4(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip)


def reasonable_host(host):
    pattern = r"^([a-zA-Z0-9](?:(?:[a-zA-Z0-9-]*|(?<!-)\.(?![-.]))*[a-zA-Z0-9]+)?)$"
    return re.match(pattern, host)


def is_port_number(port):
    return port >= 0 and port <= 65535


def resolve_ip_host(host, port):
    timeout_seconds=1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_seconds)
    try:
        result = sock.connect_ex((host,port))
    except socket.gaierror:
        return "{}:{} - Error occurred".format(host, port)
    finally:
        sock.close()
    if result == 0:
        out = "{}:{} - Open".format(host, port)
    else:
        out = "{}:{} - Closed".format(host, port)
    return out


def resolve_dns(host):
    try:
        out = f"ip: {socket.gethostbyname(host)}"
    except socket.gaierror:
        out = "ip: not resolvable"
    return out


@app.get("/", response_class=PlainTextResponse)
def root():
    response = """
Connectivity Checks:\n
host route: with get params host & port (e.g. /host?host=example.com&port=443)\n
ip route: with get params ip & port (e.g. /ip?ip=127.0.0.1&port=443)
    """
    return response


@app.get("/host", response_class=PlainTextResponse)
def host(host: Optional[str] = "", port: Optional[int] = 443):
    if not reasonable_host(host):
        return "Invalid host format"
    if not is_port_number(port):
        return "Invalid port format"
    dns = resolve_dns(host)
    connectivity = "unable to check"
    if dns.lstrip("ip: ") != "not resolvable":
        connectivity = resolve_ip_host(dns.lstrip("ip: "), port)
    response = """
host: {}\n
port: {}\n
{}\n
connectivity: {}
    """.format(host, port, dns, connectivity)
    return response


@app.get("/ip", response_class=PlainTextResponse)
def ip(ip: Optional[str] = "", port: Optional[int] = 443):
    if not is_almost_ipv4(ip):
        return "Invalid IPv4 format"
    if not is_port_number(port):
        return "Invalid port format"
    response = """
host: {}\n
port: {}\n
connectivity: {}
    """.format(ip, port, resolve_ip_host(ip, port))
    return response
