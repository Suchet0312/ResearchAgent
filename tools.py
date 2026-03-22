import requests
from bs4 import BeautifulSoup
import json

# def web_search(query:str)-> list:
#     print(f"web searching for {query}")
#     url = "https://duckduckgo.com/api/json"
#     params = {
#         "q": query,
#         "format": "json",
#         "no_redirect": 1,
#         "no_html": 1,
#     }
#     response = requests.get(url,params=params)

#     data = response.json()

#     results = []
#     for item in data.get("RelatedTopics",[])[:5]:
#         if "Text" in item and "FirstURL" in item:
#             results.append({
#                 "title":item["Text"][:80],
#                 "url":item["FirstURL"],
#                 "snippet":item["Text"]
#             })

#     return results

def web_search(query: str) -> list:
    print(f"web searching for {query}")
    try:
        from googlesearch import search
        results = []
        for url in search(query, num_results=5, sleep_interval=1):
            results.append({
                "title": url,
                "url": url,
                "snippet": ""
            })
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def fetch_page(url:str)->str:
    print(f"fetching the page {url}")

    try:
        response = requests.get(url,timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n",strip=True)
        return text[:3000]
    except Exception as e:
        return f"Error fetching page: {e}"


