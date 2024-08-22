import requests
import os
from requests.exceptions import ProxyError, SSLError, Timeout, ConnectionError

from proxy_spinner.constants import PROXY_SCRAPPER_URL


class ProxySpinner:

    def __init__(self, proxy: str = None):
        self.original_proxy = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")

        self.current_proxy = proxy or self.original_proxy
        self.used_proxies = [proxy or self.original_proxy]
        self.proxy_exhausted = False

    def get_proxy(self, max_proxies_to_test: int = 50, verbose: bool = False) -> str:

        response = requests.get(PROXY_SCRAPPER_URL)
        assert response.status_code == 200, f"Failed to get proxy list. Status code: {response.status_code}"
        response = response.json()
        assert "proxies" in response, f"Response does not contain proxies key: {response}"
        proxies = response["proxies"]
        assert len(proxies) > 0, f"Failed to get proxy list. Empty list"

        # Remove all that alive is False
        proxies = [proxy for proxy in proxies if proxy['alive']]
        # Order them by 'last_seen' (more recent first)
        proxies = sorted(proxies, key=lambda x: x['last_seen'], reverse=True)[:max_proxies_to_test]
        proxies = sorted(proxies, key=lambda x: x['timeout'])
        # Then order them by 'uptime' (largest first)
        #proxies = sorted(proxies, key=lambda x: x['uptime'], reverse=True)

        # Put the ones with 'ssl' in the front
        proxies = [proxy for proxy in proxies if proxy['ssl']] + [proxy for proxy in proxies if not proxy['ssl']]

        # Test them one by one
        for proxy_entry in proxies:

            proxy = f"{proxy_entry['ip']}:{proxy_entry['port']}"

            if proxy not in self.used_proxies and self.test_proxy(proxy, verbose=verbose):
                return proxy

        # If none of them work, return the first one
        return None

    def test_proxy(self, proxy: str, verbose: bool = False) -> bool:
        with ProxySpinner(proxy=proxy):
            try:
                response = requests.get("https://www.google.com", timeout=7)
                return response.status_code == 200
            except (ProxyError, SSLError, Timeout, ConnectionError) as e:
                if verbose:
                    print(f"Proxy {proxy} failed with error: {e}")
                return False
    def renew_proxy(self, verbose: str = False) -> str:
        self.current_proxy = self.get_proxy(verbose=verbose)
        self.used_proxies.append(self.current_proxy)
        self.proxy_exhausted = False
        return self.current_proxy

    def activate_proxy(self, renew: bool = False) -> None:
        if renew or self.proxy_exhausted:
            new_proxy = self.get_proxy()
            self.current_proxy = new_proxy
            self.used_proxies.append(new_proxy)

        if self.current_proxy is not None:
            os.environ["HTTP_PROXY"] = self.current_proxy
            os.environ["HTTPS_PROXY"] = self.current_proxy

    def deactivate_proxy(self) -> None:
        if self.original_proxy is None:
            if os.getenv("HTTP_PROXY") is not None and os.getenv("HTTPS_PROXY") is not None:
                del os.environ["HTTP_PROXY"]
                del os.environ["HTTPS_PROXY"]
        else:
            os.environ["HTTP_PROXY"] = self.original_proxy
            os.environ["HTTPS_PROXY"] = self.original_proxy

    # To use within with block
    def __enter__(self):
        self.activate_proxy(renew=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate_proxy()
        return False

