from logging.handlers import RotatingFileHandler
from cloudflare import Cloudflare
import logging
import requests


CLOUDFLARE_API_TOKEN = ""
CLOUDFLARE_ZONE_ID = ""
ACCOUNT_ID = ""
DNS_RECORD_NAME = ""

info_log=""
error_log=""

url_list = [
    "https://api.ipify.org?format=json",  # ip
    "https://ipinfo.io/json",             # ip
    "https://myip.wtf/json",              # YourFuckingIPAddress
    "https://ifconfig.me/all.json",       # ip_addr
    "https://httpbin.org/ip",             # origin
]

def getmyip():
    for url in url_list:
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            ip = data.get("ip") or data.get("origin") or data.get("YourFuckingIPAddress") or data.get("ip_addr")
            if ip:
                return ip
        except Exception as e:
            logger.error(f"Fetching failed for {url}: {e}")
    return None

def cloudflare_request():
    client = Cloudflare(api_token=CLOUDFLARE_API_TOKEN) 
    try:
        record_response = client.dns.records.list(
            zone_id=CLOUDFLARE_ZONE_ID,
        )

        for record in record_response.result:
            if record.name == DNS_RECORD_NAME:
                return record.id, record.type, record.content

    except Exception as e:
        logger.error(f"Error: {e}")

def update_dns_cloudflare(curr_ip, record_id, record_type):
    client = Cloudflare(api_token=CLOUDFLARE_API_TOKEN) 
    try:
        client.dns.records.edit(
            dns_record_id=record_id,
            zone_id=CLOUDFLARE_ZONE_ID,
            name=DNS_RECORD_NAME,
            ttl=3600,
            type=record_type,
            content=curr_ip
        )
        info_log += f"Current IP: {curr_ip} - Cloudflare IP: {record_id} - Update successfully" 
        logger.info(info_log)
    except Exception as e:
        logger.error(f"Error: {e}")



info_handler = RotatingFileHandler("ddns-info.log", maxBytes=1_000_000, backupCount=3)
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
info_handler.setFormatter(info_formatter)

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

info_handler.addFilter(InfoFilter())

error_handler = RotatingFileHandler("ddns-error.log", maxBytes=1_000_000, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)


logger = logging.getLogger()
logger.setLevel(logging.INFO)  
logger.addHandler(info_handler)
logger.addHandler(error_handler)



curr_ip = getmyip()
record_id, record_type, dns_cloudflare_ip = cloudflare_request()


if curr_ip != dns_cloudflare_ip:
    update_dns_cloudflare(curr_ip, record_id, record_type)
else:
    info_log += f"Current IP: {curr_ip} - DNS Cloudflare IP: {dns_cloudflare_ip} - No change" 
    logger.info(info_log)
