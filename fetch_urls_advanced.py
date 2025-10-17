import asyncio
import aiohttp
import json
import ssl
import certifi


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


async def fetch_urls(input_file, output_file):
    semaphore = asyncio.Semaphore(5)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    async with aiohttp.ClientSession(connector=connector) as session:
        with open(output_file, 'w') as output_f:
            for url in urls:
                async with semaphore:
                    try:
                        async with session.get(url, timeout=30) as response:
                            try:
                                json_content = await response.json()
                                result = {
                                    "url": url,
                                    "content": json_content
                                }
                            except json.JSONDecodeError:
                                result = {
                                    "url": url,
                                    "content": None,
                                    "error": 400
                                }
                            output_f.write(json.dumps(result) + '\n')
                            output_f.flush()
                    except Exception as e:
                        status_code = 500
                        for error, code in ERROR_MAP.items():
                            if isinstance(e, error):
                                status_code = code
                                break
                        result = {
                            "url": url,
                            "content": None,
                            "error": status_code
                        }
                        output_f.write(json.dumps(result) + '\n')
                        output_f.flush()


if __name__ == '__main__':
    asyncio.run(fetch_urls('urls.txt', 'results_advanced.jsonl'))
