from banner import banner
import aiohttp
import asyncio
import argparse

# banner
banner.marsias_pan_banner()

async def fetch(session, url):
    try:
        # 
        async with session.get(url, timeout=5) as response:
            
            if response.status_code == 200:
             print(f"[+] Discovered subdomain: {url}")
             return url
            elif response.status_code == 301:
             print(f"[+] Subdomain {url} permanently moved (Status 301)")
             return url
            elif response.status_code == 302:
             print(f"[+] Subdomain {url} temporarily moved (Status 302)")
             return url
            elif response.status_code == 500:
             print(f"[?] Internal server error on {url} (Status 500)")
             return None
            elif response.status_code == 503:
             print(f"[?] Service unavailable on {url} (Status 503)")
             return None
    except Exception as e:
        # 
        http_url = url.replace("https://", "http://")
        try:
            async with session.get(http_url, timeout=5) as response:
                if response.status == 200:
                    print(f"[+] Discovered subdomain: {http_url}")
                    return http_url
        except Exception as e:
            return None  # 







async def fetch_all_subdomains(domain, subdomains):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for subdomain in subdomains:
            url = f"https://{subdomain}.{domain}"
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        
        discovered_subdomains = await asyncio.gather(*tasks)
        return [subdomain for subdomain in discovered_subdomains if subdomain]  # 
    



    

def parse_arguments():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration")
    
    parser.add_argument('-u', '--url', type=str, help="Subdomain taraması yapılacak domain", required=True)
    parser.add_argument('-s', '--subdomains', action='store_true', help="Subdomainleri listele")
    parser.add_argument('-w', '--file', type=str, help="Subdomainleri içeren dosyanın yolu", required=True)
    
    args = parser.parse_args()
    
    return args

def main():
    args = parse_arguments()

    domain = args.url
    file = args.file

    banner.marsias_pan_banner()

    # 
    with open(file, 'r') as f:
        content = f.read()
        subdomains = content.splitlines()

    # 
    discovered_subdomains = asyncio.run(fetch_all_subdomains(domain, subdomains))

    # 
    with open("discovered_subdomains.txt", "w") as f:
        for subdomain in discovered_subdomains:
            f.write(subdomain + "\n")

if __name__ == "__main__":
    main()
