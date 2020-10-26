
######################################################################################
#################  A simple script to check whether a list of urls  ##################
#################  is valid or not, can be used during information  ##################
################# gathering stage in a pentest to produce a refined ##################
#################                 list of targets.                  ##################
######################################################################################


from sys import argv
import requests
import urllib3

#supresses the insecure ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(argv) != 2:
    print("Usage: python link-checker.py file.txt")
    exit(1)

filename = argv[1]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8',
              'Accept-Encoding': 'gzip',}


with open(filename, 'r') as f:
    """ 
        Reads the file and stores it in a list, every element is a url
    """
    results = f.read().splitlines()
    
    #Clears empty strings (courtsey of stackoverflow)
    results = list(filter(None, results))
    
for link in results:
    """
        using the requests module it sends a get request to the every url in the list
        and if no exception occurs it will print the status code
    """
    
    #TODO-1: make it output urls that responds with 200 in a file (may include an option to add other respnse codes)
    #TODO-2: Add option to check if the url returns a meaningful response by checking content-length header
    try:
        response = requests.get("http://" + link, headers=headers, timeout=8, verify=False)
    except requests.exceptions.Timeout:
        print(f"Cannot connect to {link}: request time-out")
    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to {link}: Connection Error")
    except requests.exceptions.HTTPError:
        print(f"Cannot connect to {link}: invalid HTTP response")
    except requests.exception.RequestException:
        print(f"Cannot connect to {link}: Unknown Error")
    else:
        print(f"{link} responded with statuse code: {response.status_code}")
    