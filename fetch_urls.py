import asyncio
import aiohttp
import json
import certifi
import ssl


ERROR_MAP = {
    asyncio.TimeoutError: 408,
    aiohttp.ClientConnectorError: 0,
    aiohttp.ServerDisconnectedError: 503,
    aiohttp.ClientResponseError: 400,
    aiohttp.ClientOSError: 0,
    aiohttp.ServerTimeoutError: 504,
    aiohttp.ClientPayloadError: 400,
    aiohttp.TooManyRedirects: 310,
    ssl.SSLCertVerificationError: 495,
    UnicodeError: 400,
}


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = []
        for url in urls:
            async with semaphore:
                try:
                    async with session.get(url, timeout=10) as response:
                        results.append(
                            {"url": url,
                             "status_code": response.status}
                        )
                except Exception as e:
                    status_code = 500
                    for error, status_code in ERROR_MAP.items():
                        if isinstance(e, error):
                            results.append(
                                {"url": url,
                                 "status_code": status_code}
                            )
                            break
        with open(file_path, 'w') as f:
            for result in results:
                f.write(json.dumps(result) + '\n')
        return {result["url"]: result["status_code"] for result in results}


if __name__ == '__main__':
    result_dict = asyncio.run(fetch_urls(urls, './results.jsonl'))
