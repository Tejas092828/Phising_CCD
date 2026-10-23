import re
from urllib.parse import urlparse

def extract_features(url: str) -> dict:
    """
    Extracts advanced lexical and structural features.
    Upgraded to 14 features to hit >90% accuracy and >0.88 F1-Score.
    """
    url = str(url).strip()
    
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            parsed_url = urlparse('http://' + url)
        else:
            parsed_url = urlparse(url)
            
        domain = parsed_url.netloc
        path = parsed_url.path
    except ValueError:
        domain = ""
        path = url
        
    features = {}
    
    # 1. Length metrics
    features['URL_Length'] = len(url)
    features['Domain_Length'] = len(domain)
    features['Path_Length'] = len(path)
    
    # 2. Count metrics
    features['Num_Dots'] = url.count('.')
    features['Num_Hyphens'] = url.count('-')
    
    special_chars = ['?', '=', '_', '&', '%', ';', '~']
    features['Num_Special_Chars'] = sum(1 for c in url if c in special_chars)
    
    features['Num_Digits'] = sum(1 for c in url if c.isdigit())
    features['Num_Letters'] = sum(1 for c in url if c.isalpha())
    features['Num_Vowels'] = sum(1 for c in url.lower() if c in 'aeiou')
    
    # 3. Structural metrics
    clean_domain = domain.split(':')[0] if domain else ""
    ip_pattern = re.compile(r'^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])$')
    features['Has_IP'] = 1 if ip_pattern.match(clean_domain) else 0
    
    features['Has_At_Symbol'] = 1 if '@' in url else 0
    features['Domain_Depth'] = path.count('/')
    features['Num_Subdomains'] = domain.count('.')
    
    # 4. Social Engineering / Suspicious Words
    suspicious_words = ['login', 'verify', 'update', 'secure', 'bank', 'account', 'signin', 'recover', 'free', 'bonus', 'admin']
    features['Suspicious_Words'] = sum(1 for w in suspicious_words if w in url.lower())
    
    return features