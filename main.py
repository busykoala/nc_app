from typing import Optional
import socket

from fastapi import FastAPI


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


def resolve_dns(url):
    try:
        out = {"ip": socket.gethostbyname(url)}
    except socket.gaierror:
        out = {"ip": "not resolvable"}
    return out


@app.get("/")
def root():
    response = {
        "/url": "with get params url/port",
        "/ip": "with get params ip/port",
    }
    return response


@app.get("/url")
def url(url: Optional[str] = "", port: Optional[int] = 443):
    dns = resolve_dns(url)
    connectivity = "unable to check"
    if dns["ip"] != "not resolvable":
        connectivity = resolve_ip_host(dns["ip"], port)
    response = {
        "url": url,
        "port": port,
        "dns": dns["ip"],
        "connectivity": connectivity,
    }
    return response


@app.get("/ip")
def ip(ip: Optional[str] = "", port: Optional[int] = 443):
    response = {
        "ip": ip,
        "port": port,
        "connectivity": resolve_ip_host(ip, port),
    }
    return response
