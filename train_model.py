import pandas as pd
import numpy as np
import re
import joblib
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Feature Extraction
def extract_features(url):
    features = []
    
    # Length of URL
    features.append(len(url))
    
    # Count of dots
    features.append(url.count('.'))
    
    # Presence of @
    features.append(1 if '@' in url else 0)
    
    # Presence of IP address
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)
    
    # Suspicious keywords
    suspicious_keywords = ['login','verify','secure','update','bank','account']
    features.append(sum(keyword in url.lower() for keyword in suspicious_keywords))
    
    # Number of subdirectories
    path = urlparse(url).path
    features.append(path.count('/'))
    
    return features

# Load Dataset
df = pd.read_csv("phishing_dataset.csv")

X = []
for url in df['url']:
    X.append(extract_features(url))

X = np.array(X)
y = df['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train,y_train)

# Accuracy
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test,pred))

joblib.dump(model,"model.pkl")
