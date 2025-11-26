---

✅ **What This Script Does**

The file **error_misconfig_scanner.py** is a **basic web error & misconfiguration scanner**.
It checks a target URL for:

**1. Technology / Server Information Leakage**

It sends a GET request and extracts important headers:

* `Server`
* `X-Powered-By`
* `X-AspNet-Version`
* `X-Runtime`

If these appear, the server is leaking version info.

---

**2. Sensitive Files / Paths Exposure**

It checks common dangerous paths:

```
/phpinfo.php
/server-info
/server-status
/.env
/config.php
/backup.zip
/db.sql
/.git/
...
```

If the target returns `200 OK` with meaningful content →
⚠️ **You found exposed files/directories**.

---

**3. Error-based Vulnerabilities**

It injects **error-triggering payloads** to test error handling:

Examples:

```
'
"
<test>
../../../etc/passwd
{{7*7}}
%7B%7B7*7%7D%7D
```

If the server returns error keywords such as:

```
warning
fatal
mysql
traceback
sqlstate
undefined
pdoexception
templatesyntaxerror
```

=> ⚠️ **Error leakage found**
→ Possible SQLi, Template Injection, Path Traversal, etc.

---

**4. Dangerous HTTP Methods**

It sends an OPTIONS request to check enabled methods:

* PUT
* DELETE
* TRACE
  → These are dangerous if enabled.

---

🧠 **How the Script Works (Step-by-step)**

| Step | Function                   | What it Does                          |
| ---- | -------------------------- | ------------------------------------- |
| 1    | `check_headers()`          | Identifies server info leakage        |
| 2    | `test_common_paths()`      | Scans sensitive/exposed files         |
| 3    | `trigger_error_payloads()` | Tests for verbose error handling      |
| 4    | `check_http_methods()`     | Detects risky HTTP methods            |
| 5    | `main()`                   | Handles CLI input and runs all checks |

---

🖥️ **How to Run This Script**

**1. Save the script**

If not already saved:

```
error_misconfig_scanner.py
```

---

**2. Install dependencies**

It uses only `requests`, which may need installing:

```bash
pip3 install requests
```

---

**3. Run the script**

Syntax:

```bash
python3 error_misconfig_scanner.py https://target.com
```

Example:

```bash
python3 error_misconfig_scanner.py https://example.com
```

---

📌 **Sample Output (What You Might See)**

```
============================================================
Custom Error Handling & Misconfiguration Scanner
============================================================
Target: https://example.com

[1] Checking Server Headers
[+] Server: Apache/2.4.29
[+] X-Powered-By: PHP/7.4.3

[2] Testing Sensitive Paths & Directories
[!!!] Sensitive path exposed → https://example.com/phpinfo.php
[!!!] Sensitive path exposed → https://example.com/.env

[3] Triggering Error Payloads
[!!!] Error message leaked → Found keyword: mysql

[4] Checking Allowed HTTP Methods
[!!!] Dangerous HTTP method enabled: TRACE
```

---

⭐ **What This Script Helps You Detect**

✔ Misconfigurations

✔ Error leaks (debug mode)

✔ Exposed backups

✔ Info leakage

✔ Sensitive files

✔ Misconfigured methods

✔ Possible SQL/XSS/LFI clues

Perfect as a lightweight recon + bug bounty helper.

---
