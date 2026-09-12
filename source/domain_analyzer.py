import whois
import datetime
import tldextract
from typing import Dict, Any


def get_domain_info(url: str) -> Dict[str, Any]:
    extracted = tldextract.extract(url)

    domain = extracted.domain

    try:
        response = whois.whois(f"{domain}.{extracted.suffix}")

        creation_date = response.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age = (datetime.datetime.now() - creation_date).days

        owner = response.registrant_name

        return {
            "domain": f"{domain}.{extracted.suffix}",
            "age": age,
            "owner": owner,
            "error": None
        }
    except Exception as err:
        return {
            "domain": "",
            "age": -1,
            "owner": "",
            "error": err
        }
