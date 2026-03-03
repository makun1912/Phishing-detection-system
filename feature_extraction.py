import re
import math
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])

def extract_features(url):
    features = []
    parsed = urlparse(url)

    features.append(len(url))
    features.append(len(parsed.netloc))
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(sum(c.isdigit() for c in url))
    features.append(1 if '@' in url else 0)
    features.append(1 if parsed.scheme == 'https' else 0)

    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    features.append(1 if re.search(ip_pattern, parsed.netloc) else 0)

    suspicious = ['login', 'verify', 'bank', 'update', 'free']
    features.append(1 if any(word in url.lower() for word in suspicious) else 0)

    features.append(entropy(url))

    try:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, 'html.parser')
        features.append(len(soup.find_all('form')))
        features.append(len(soup.find_all('input', type='password')))
    except:
        features.extend([0, 0])

    return features
