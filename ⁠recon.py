#!/usr/bin/env python3
import asyncio
import aiohttp
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""{Fore.CYAN}
   _____ subCheck v1.0 _____
  [ Fast Subdomain & Status Checker ]
{Style.RESET_ALL}"""

async def check_domain(session, domain):
    urls = [f"http://{domain}", f"https://{domain}"]
    for url in urls:
        try:
            async with session.get(url, timeout=4, ssl=False) as response:
                status = response.status
                color = Fore.GREEN if status == 200 else Fore.YELLOW if status < 400 else Fore.RED
                print(f"[{color}{status}{Style.RESET_ALL}] -> {url}")
                return
        except Exception:
            continue
    print(f"[{Fore.RED}DOWN{Style.RESET_ALL}] -> {domain}")

async def main(file_path):
    print(BANNER)
    try:
        with open(file_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File not found: {file_path}")
        return

    print(f"{Fore.BLUE}[*] Testing {len(domains)} targets...\n")
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_domain(session, d) for d in domains]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fast Async Subdomain Status Checker")
    parser.add_argument("-f", "--file", required=True, help="Path to file containing subdomains")
    args = parser.parse_args()
    
    asyncio.run(main(args.file))
