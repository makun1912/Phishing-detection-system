import pandas as pd

# Load real phishing URLs from OpenPhish
with open("feed.txt", "r") as f:
    phishing_urls = f.read().splitlines()

# Limit to first 500
phishing_urls = phishing_urls[:500]

# Legitimate URLs
legit_urls = [
    "https://google.com",
    "https://facebook.com",
    "https://amazon.com",
    "https://microsoft.com",
    "https://apple.com",
    "https://github.com",
    "https://linkedin.com",
    "https://netflix.com",
    "https://twitter.com",
    "https://wikipedia.org"
]

# Repeat legit URLs to balance dataset
legit_urls = legit_urls * 50

data = []

for url in phishing_urls:
    data.append([url, 1])

for url in legit_urls:
    data.append([url, 0])

df = pd.DataFrame(data, columns=["url", "label"])
df.to_csv("phishing_dataset.csv", index=False)

print("✅ Dataset generated successfully.")
print("Total rows:", len(df))
