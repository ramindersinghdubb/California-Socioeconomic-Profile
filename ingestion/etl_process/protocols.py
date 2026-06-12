"""
HTTPS GET methods.
"""

import requests as req



def fetch_content(url: str):
    """
    Synchronous method to fetch the JSON content for a(n) URL.
    """
    resp = req.get(url)
    try:
        return resp.json()
    except:
        msg = f'Error; HTTPS Status {resp.status_code}. ' + f'Response Text:\n{resp.text}'
        raise req.ConnectionError(msg) from None