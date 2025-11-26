import requests
import sys
import urllib3
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMMON_ERROR_PAYLOADS = [
    "'", "\"", "<test>", "../../../etc/passwd", "{{7*7}}", "%7B%7B7*7%7D%7D"
]

COMMON_PATHS = [
    "/phpinfo.php",
    "/server-info",
    "/server-status",
    "/.env",
    "/config.php",
    "/backup.zip",
    "/db.sql",
    "/error",
    "/debug",
    "/debug/trace",
    "/admin/",
    "/uploads/",
    "/.git/"
]

ERROR_KEYWORDS = [
    "warning", "fatal", "exception", "traceback", "mysql", "syntax error",
    "undefined", "stack trace", "runtime error", "include()", "failed to open stream",
    "NullReference", "ReferenceError", "ErrorException", "PDOException",
    "SQLSTATE", "Debug mode", "TemplateSyntaxError"
]

HEADERS_OF_INTEREST = [
    "Server", "X-Powered-By", "X-AspNet-Version", "X-Runtime"
]

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def check_headers(url):
    print_header("[1] Checking Server Headers")
    try:
        r = requests.get(url, verify=False, timeout=10)
        for h in HEADERS_OF_INTEREST:
            if h in r.headers:
                print(f"[+] {h} : {r.headers[h]}")
        print("✔ Header check completed.")
    except:
        print("✘ Could not fetch headers.")

def test_common_paths(url):
    print_header("[2] Testing Sensitive Paths & Directories")
    for path in COMMON_PATHS:
        full_url = urljoin(url, path)
        try:
            r = requests.get(full_url, verify=False, timeout=10)
            if r.status_code == 200 and len(r.text) > 30:
                print(f"[!!!] Sensitive path exposed → {full_url}")
        except:
            pass
    print("✔ Path tests completed.")

def trigger_error_payloads(url):
    print_header("[3] Triggering Error Payloads to Check Error Handling")
    for payload in COMMON_ERROR_PAYLOADS:
        test_url = f"{url}?test={payload}"
        try:
            r = requests.get(test_url, verify=False, timeout=10)
            body = r.text.lower()
            for e in ERROR_KEYWORDS:
                if e in body:
                    print(f"[!!!] Error message leaked on: {test_url}")
                    print(f" → Found keyword: {e}")
        except:
            pass
    print("✔ Error payload tests completed.")

def check_http_methods(url):
    print_header("[4] Checking Allowed HTTP Methods")
    try:
        r = requests.options(url, verify=False, timeout=10)
        if "allow" in r.headers:
            print("[+] Allowed Methods:", r.headers["allow"])
            if any(x in r.headers["allow"] for x in ["PUT", "DELETE", "TRACE"]):
                print("[!!!] Dangerous HTTP method enabled!")
        else:
            print("No method information found.")
    except:
        print("✘ OPTIONS method failed.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 error_misconfig_scanner.py https://target.com")
        sys.exit(1)

    url = sys.argv[1]
    
    print_header("Custom Error Handling & Misconfiguration Scanner")
    print(f"Target: {url}")

    check_headers(url)
    test_common_paths(url)
    trigger_error_payloads(url)
    check_http_methods(url)

    print_header("Scan Complete")

if __name__ == "__main__":
    main()