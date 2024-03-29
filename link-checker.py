
######################################################################################
#################  A simple script to check whether a list of urls  ##################
#################  is valid or not, can be used during information  ##################
################# gathering stage in a pentest to produce a refined ##################
#################                 list of targets.                  ##################
######################################################################################


from sys import argv
import os
import requests
import urllib3
from queue import Queue
from threading import Thread

NUM_WORKERS = os.cpu_count()
task_queue = Queue()

# supresses the insecure ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8',
              'Accept-Encoding': 'gzip'}


valid_http = []
invalid_http = []


def check_link(link):
    try:
        response = requests.get("http://" + link, headers=headers, timeout=8, verify=False)
    except requests.exceptions.Timeout:
        invalid_http.append(f"Cannot connect to {link}: request time-out\n")
    except requests.exceptions.ConnectionError:
        invalid_http.append(f"Cannot connect to {link}: Connection Error\n")
    except requests.exceptions.HTTPError:
        invalid_http.append(f"Cannot connect to {link}: invalid HTTP response\n")
    except requests.exceptions.RequestException:
        invalid_http.append(f"Cannot connect to {link}: Unknown Error\n")
    except requests.exceptions.TooManyRedirects:
        invalid_http.append(f"cannot connect to {link}: too many redirects\n")
    else:
        valid_http.append(f"{link} responded with statuse code: {response.status_code}\n")


def worker():
    while True:
        link = task_queue.get()
        check_link(link)
        task_queue.task_done()
        if task_queue.empty():
            break

if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage: python link-checker.py file.txt")
        exit(1)

    filename = argv[1]

    with open(filename, 'r') as f:

        """
            Reads the file and stores it in a list, every element is a url
        """
        results = f.read().splitlines()
        results = list(filter(None, results))

        try:
            threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
            [task_queue.put(link) for link in results]
            [thread.start() for thread in threads]
            task_queue.join()

        except KeyboardInterrupt:
            print("\nYou pressed Ctrl+C")
            print("Exiting without saving")
            exit(2)

        # Output links with valid http response code in one file
        with open("valid.txt", 'w') as out:
            out.writelines(valid_http)

        # Output links with invalid http responses in one file
        with open("invalid.txt", 'w') as out:
            out.writelines(invalid_http)
