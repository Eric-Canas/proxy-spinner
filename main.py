import requests
from proxy_spinner.proxy_spinner import ProxySpinner


if __name__ == '__main__':
    # Get my location:
    get_location_url = "https://cmp.inmobi.com/geoip"

    # Without proxy
    response = requests.get(get_location_url, timeout=10).json()
    print(f"Without Proxy: {response['city']} ({response['country']})")

    # Get a proxy
    proxy_spinner = ProxySpinner()
    proxy = proxy_spinner.renew_proxy(verbose=True)
    # With proxy
    with proxy_spinner:
        response = requests.get(get_location_url, timeout=10).json()
        print(f"With Proxy: {response['city']} ({response['country']}) [Proxy: {proxy}]")

    # Without proxy
    response = requests.get(get_location_url, timeout=10).json()
    print(f"Without Proxy: {response['city']} ({response['country']})")

    proxy = proxy_spinner.renew_proxy(verbose=True)

    # With proxy
    with proxy_spinner:
        response = requests.get(get_location_url, timeout=10).json()
        print(f"With New Proxy: {response['city']} ({response['country']}) [Proxy: {proxy}]")
