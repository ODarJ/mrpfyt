import os
import sys
import re
import json
import urllib.request

SRT_PATH = sys.argv[1]
OUT_PATH = sys.argv[2]
API_KEY = os.environ["LLM_API_KEY"]

with open(SRT_PATH, encoding="utf-8") as f:
    raw = f.read()

lines = raw.splitlines()
texts = []
for ln in lines:
    s = ln.strip()
    if not s: continue
    if s.isdigit(): continue
    if "-->" in s: continue
    texts.append(s)

joined = "\n".join(texts)

prompt = (
    "Translate the following movie narration into natural spoken Burmese. "
    "Keep it concise and conversational, suitable for a movie recap video. "
    "Preserve line breaks between separate lines. "
    "Only return the translation, no explanations.\n\n" + joined
)

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={API_KEY}"
)
body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
req = urllib.request.Request(
    url, data=body, headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req, timeout=180) as r:
    data = json.load(r)

out = data["candidates"][0]["content"]["parts"][0]["text"]

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(out)

print("Translated chars:", len(out))