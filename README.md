# Cloudflare DDNS Updater

A lightweight Python script that automatically keeps your Cloudflare DNS record in sync with your current public IP address — perfect for self-hosted servers on dynamic IP connections.

---

## How It Works

1. Fetches your current public IP from a list of fallback providers
2. Retrieves the current IP stored in your Cloudflare DNS record
3. Updates the DNS record only if the IP has changed
4. Logs all activity to rotating log files

---

## Requirements

- Python 3.7+
- A Cloudflare account with an existing DNS A record

### Dependencies

```
cloudflare
requests
```

Install with:

```bash
pip install cloudflare requests
```

---

## Configuration

Open the script and fill in the following constants at the top:

| Variable               |                     Description                                |
|                        |                                                                |
| `CLOUDFLARE_API_TOKEN` | Your Cloudflare API token (needs DNS Edit permission)          |    
| `CLOUDFLARE_ZONE_ID`   | The Zone ID of your domain (found in the Cloudflare dashboard) |
| `ACCOUNT_ID`           | Your Cloudflare Account ID                                     |
| `DNS_RECORD_NAME`      | The full DNS record name to update (e.g. `home.example.com`)   |

### Getting a Cloudflare API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → **My Profile** → **API Tokens**
2. Click **Create Token**
3. Use the **Edit zone DNS** template
4. Scope it to the specific zone you want to manage
5. Copy the generated token into `CLOUDFLARE_API_TOKEN`

---

## Usage

Run the script manually:

```bash
python ddns_updater.py
```

### Automating with Cron (Linux/macOS)

To run every 5 minutes, add this to your crontab (`crontab -e`):

```
*/5 * * * * /usr/bin/python3 /path/to/ddns_updater.py
```

### Automating with Task Scheduler (Windows)

Create a basic task in **Task Scheduler** that runs `python ddns_updater.py` on your desired schedule.

---

## Logging

The script writes to two rotating log files (max 1 MB each, 3 backups kept):

| File             |             Contents                            |
|                  |                                                 |
| `ddns-info.log`  | Successful updates and no-change events         |
| `ddns-error.log` | Errors from IP fetching or Cloudflare API calls |

Example log entries:

```
2025-01-15 10:32:01 - INFO - Current IP: 203.0.113.42 - DNS Cloudflare IP: abc123 - Update successfully
2025-01-15 10:37:01 - INFO - Current IP: 203.0.113.42 - DNS Cloudflare IP: 203.0.113.42 - No change
```

---

## IP Detection

The script queries multiple public IP providers in order, using the first successful response:

- `api.ipify.org`
- `ipinfo.io`
- `myip.wtf`
- `ifconfig.me`
- `httpbin.org`

This provides resilience if any single provider is unavailable.

---

## Notes

- The script is stateless — it queries Cloudflare on every run rather than caching state locally
- Only the record matching `DNS_RECORD_NAME` is updated; all other records are untouched
- TTL is set to **3600 seconds** on each update
