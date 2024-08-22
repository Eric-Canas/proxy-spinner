import requests
from proxy_rotator.proxy_rotator import ProxyRotator


if __name__ == '__main__':
    # Get my location:
    get_location_url = "https://cmp.inmobi.com/geoip"

    # Get a proxy
    proxy_rotator = ProxyRotator()
    proxy = proxy_rotator.renew_proxy(verbose=True)

    # Without proxy
    response = requests.get(get_location_url, timeout=10).json()
    print(f"Without Proxy: {response['city']} ({response['country']})")

    # With proxy
    with proxy_rotator:
        response = requests.get(get_location_url, timeout=10).json()
        print(f"With Proxy: {response['city']} ({response['country']}) [Proxy: {proxy}]")

    # Without proxy
    response = requests.get(get_location_url, timeout=10).json()
    print(f"Without Proxy: {response['city']} ({response['country']})")

    proxy = proxy_rotator.renew_proxy(verbose=True)

    # With proxy
    with proxy_rotator:
        response = requests.get(get_location_url, timeout=10).json()
        print(f"With New Proxy: {response['city']} ({response['country']}) [Proxy: {proxy}]")
