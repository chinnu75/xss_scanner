

````markdown
# XSS Scanner GUI

A Python-based XSS (Cross-Site Scripting) vulnerability scanner with a graphical user interface.

---

## Features

- Scan web pages for XSS vulnerabilities by testing multiple payloads.
- Supports over 100 common XSS payloads for thorough scanning.
- Visual results with color-coded highlighting for detected vulnerabilities.
- Multi-threaded scanning for responsive GUI during scans.
- Extracts and tests all forms present on the target webpage.

---

## Technologies Used

- Python 3
- Tkinter for GUI
- Requests for HTTP requests
- BeautifulSoup4 for HTML parsing

---

## Installation

1. Clone this repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/xss-scanner-gui.git
   cd xss-scanner-gui
````

2. Install the required Python packages:

   ```bash
   pip install requests beautifulsoup4
   ```

---

## Usage

1. Run the scanner script:

   ```bash
   python xss_scanner_gui.py
   ```
2. Enter the target URL in the input field.
3. Click the **Scan** button.
4. Watch the scanning progress and results in the output panel.
5. Vulnerable forms will be highlighted in red along with the payload detected.

---

## Notes

* Make sure the URL is valid and reachable.
* Only scan websites you have permission to test.
* This tool tests for reflected XSS vulnerabilities by injecting payloads into form inputs.

---

## Author

**Kasturi Bharadwaj**

LinkedIn: [https://www.linkedin.com/in/bharadwaj-kasturi-451a031a9](https://www.linkedin.com/in/bharadwaj-kasturi-451a031a9)

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

```

---

If you want, I can prepare the `LICENSE` file content for you too!
```
