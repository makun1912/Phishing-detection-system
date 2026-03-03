from flask import Flask, render_template, request
import joblib
import numpy as np
import re
from urllib.parse import urlparse
import datetime
import whois

app = Flask(__name__)
model = joblib.load("model.pkl")

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if '@' in url else 0)
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)
    
    suspicious_keywords = ['login','verify','secure','update','bank','account']
    features.append(sum(keyword in url.lower() for keyword in suspicious_keywords))
    
    path = urlparse(url).path
    features.append(path.count('/'))
    
    return features

def check_zero_day(url):
    try:
        domain_info = whois.whois(url)
        creation_date = domain_info.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        age = (datetime.datetime.now() - creation_date).days
        
        if age < 30:
            return True, age
        else:
            return False, age
    except:
        return False, "Unknown"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        
        features = np.array([extract_features(url)])
        prediction = model.predict(features)[0]
        confidence = round(max(model.predict_proba(features)[0]) * 100,2)
        
        zero_day, age = check_zero_day(url)
        
        if prediction == 1:
            result = "PHISHING"
            if zero_day:
                category = "Zero-Day Attack"
            else:
                category = "Known Phishing"
        else:
            result = "LEGITIMATE"
            category = "Safe Website"
        
        return render_template("index.html",
                               url=url,
                               result=result,
                               confidence=confidence,
                               category=category,
                               age=age)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
