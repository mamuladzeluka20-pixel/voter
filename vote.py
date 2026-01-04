import urllib.parse
import sys

def vote(url_param):
    """
    Process voting with a URL parameter
    
    Args:
        url_param (str): URL parameter containing voting data
    """
    try:
        # Parse the URL parameter
        parsed = urllib.parse.urlparse(url_param)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        print(f"URL Parameter received: {url_param}")
        print(f"Parsed parameters: {query_params}")
        
        return True
    except Exception as e:
        print(f"Error processing URL parameter: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_parameter = sys.argv[1]
        vote(url_parameter)
    else:
        print("Usage: python vote.py <url_parameter>")
