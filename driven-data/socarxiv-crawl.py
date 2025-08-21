# pip install requests beautifulsoup4 lxml transformers torch --upgrade
import json, re, textwrap, requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def fetch_page(url:str)->str:
    r = requests.get(url, timeout=20, headers={"User-Agent":"CalGeekBot/0.1"})
    r.raise_for_status()
    return r.text

def extract_title_and_abstract(html:str):
    soup = BeautifulSoup(html, "lxml")
    # 1) Try JSON-LD (often present on OSF/SocArXiv)
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string)
            if isinstance(data, dict): data=[data]
            for d in data:
                if str(d.get("@type","")).lower() in {"scholarlyarticle","creativework","article"}:
                    title = d.get("name") or d.get("headline")
                    abstract = d.get("description") or d.get("abstract")
                    if title and abstract:
                        return title.strip(), abstract.strip()
        except Exception: pass
    # 2) Fallback to meta
    meta = soup.find("meta", attrs={"name":"description"}) or soup.find("meta", property="og:description")
    abstract = meta["content"].strip() if meta and meta.get("content") else None
    title = (soup.title.string or "").strip() if soup.title else None
    # 3) Last resort: text near “Abstract”
    if not abstract:
        txt = soup.get_text("\n", strip=True)
        m = re.search(r"Abstract[:\s]+(.{200,2000}?)\n\n", txt, re.IGNORECASE|re.DOTALL)
        abstract = m.group(1).strip() if m else None
    return title, abstract

def summarize(text:str, max_words=120):
    model_id = "sshleifer/distilbart-cnn-12-6"  # fast, decent
    pipe = pipeline("summarization", model=model_id, tokenizer=model_id, truncation=True)
    out = pipe(text, max_length=180, min_length=60, do_sample=False)[0]["summary_text"]
    return "\n".join(textwrap.wrap(out, 100))

if __name__ == "__main__":
    url = "https://osf.io/preprints/socarxiv/unq6y_v2"
    html = fetch_page(url)
    title, abstract = extract_title_and_abstract(html)
    print("TITLE:", title or "(unknown)")
    if not abstract:
        raise SystemExit("No abstract found; try another URL or add PDF parsing.")
    print("\nSUMMARY:\n", summarize(abstract))
