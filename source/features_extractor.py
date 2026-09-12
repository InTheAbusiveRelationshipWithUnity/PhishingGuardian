import tldextract
import math
from typing import Dict, Union


def shennon_entropy(text: str) -> float:
    if not text:
        return 0.0
    
    p = [text.count(symbol) / len(text) for symbol in list(set(text))]

    return - sum([prob * math.log(prob) / math.log(2) for prob in p])


def extract_features(url: str) -> Dict[str, Union[int, float]]:
    domain = tldextract.extract(url).domain
    subdomains = tldextract.extract(url).subdomain

    special_symbols = set("-@_?=%&=#+")
    special_symbols_count = sum(1 for char in url if char in special_symbols)
    
    return {
        "url": url,
        "url_len": len(url),
        "domain_length": len(domain),
        "count_digits": sum(s.isdigit() for s in url),
        "special_symbols": special_symbols_count,
        "count_dots": url.count("."),
        "count_and": url.count("&"),
        "count_or": url.count("|"),
        "ip": 1 if domain.count(".") > 1 and domain.replace(".", "").isdigit() else 0,
        "entropy_url": shennon_entropy(url),
        "entropy_domain": shennon_entropy(domain),
        "subdomain": len(subdomains.split(".")) if subdomains else 0,
        "is_https": 1 if url.startswith("https") else 0,
        "path_depth": url.count("/")
    }
