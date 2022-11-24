from typing import Optional
import socket

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()


def resolve_ip_host(host, port):
    timeout_seconds=1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_seconds)
    result = sock.connect_ex((host,port))
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
    dns = resolve_dns(host)
    connectivity = "unable to check"
    if dns.lstrip("ip: ") != "not resolvable":
        connectivity = resolve_ip_host(dns.lstrip("ip: "), port)
    response = """
host: {}\n
port: {}\n
{}\n,
connectivity: {}
    """.format(host, port, dns, connectivity)
    return response


@app.get("/ip", response_class=PlainTextResponse)
def ip(ip: Optional[str] = "", port: Optional[int] = 443):
    response = """
host: {}\n
port: {}\n
connectivity: {}
    """.format(ip, port, resolve_ip_host(ip, port))
    return response
