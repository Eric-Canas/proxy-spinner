'ProxyRotator is an straightforward, non-reliable, non-secure, but easy-to-use library for '
                'avoiding IP blocking by rotating free proxies on demand. It relies in services like '
                'proxyscrape.com to get the proxies and rotates them on demand, and is subject to the '
                'availability of that service and the proxies it lists.',

# Proxy Rotator

ProxyRotator is an straightforward, *non-reliable*, *non-secure*, but easy-to-use library for avoiding IP blocking 
by rotating free proxies on demand. It relies in services like [ProxyScrape.com](https://proxyscrape.com/free-proxy-list) to get the proxies and 
rotate them on demand, and is subject to the availability of that service and the proxies it lists.

## Installation

```bash
pip install proxy-rotator
```

## Usage

```python
from proxy_spinner import ProxySpinner
import requests

# Initialize the proxy rotator. By default it uses no proxy until you call renew_proxy
proxy_manager = ProxySpinner()
# Renew the proxy to use a new one. Could take a while to find a working one
found_proxy = proxy_manager.renew_proxy()

# Use the proxy in your requests within a context manager
with proxy_manager:
    response = requests.get("https://cmp.inmobi.com/geoip").json()
    print(f"PROXY ENABLED: You are at  {response['city']} ({response['country']}) "
          "[Proxy: {found_proxy}]")

# Without the context manager, the proxy is not used
response = requests.get("https://cmp.inmobi.com/geoip").json()
print(f"PROXY DISABLED: You are at  {response['city']} ({response['country']})")
```

Output: 
```
PROXY ENABLED: You are at budapest (hun) [Proxy: 178.48.68.61:18080]
PROXY DISABLED: You are at ********** (esp)
```