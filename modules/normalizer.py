import re

def extract_numbers_and_dates(slide_data):
    facts = []
    all_texts = slide_data["texts"] + [img["ocr_text"] for img in slide_data["images"] if img["ocr_text"]] + [slide_data["notes"]]

    for text in all_texts:
        if not text:
            continue

        for m in re.finditer(r"\$?\d[\d,]*(?:\.\d+)?\s?(M|B|K)?", text):
            raw = m.group()
            val = normalize_currency(raw)
            facts.append({"type": "currency", "value": val, "raw": raw, "context": text})

        for m in re.finditer(r"\d+(\.\d+)?\s?%", text):
            facts.append({"type": "percent", "value": float(m.group().replace("%", "")), "raw": m.group(), "context": text})

        for m in re.finditer(r"\d+\s?(mins?|hours?|hrs?)", text, re.I):
            facts.append({"type": "duration", "value": m.group(), "raw": m.group(), "context": text})

        for m in re.finditer(r"\d+x", text, re.I):
            facts.append({"type": "multiplier", "value": m.group(), "raw": m.group(), "context": text})

    return facts

def normalize_currency(raw):
    s = raw.replace("$", "").replace(",", "").strip()
    mult = 1
    if s.lower().endswith("m"):
        mult = 1_000_000
        s = s[:-1]
    elif s.lower().endswith("b"):
        mult = 1_000_000_000
        s = s[:-1]
    elif s.lower().endswith("k"):
        mult = 1_000
        s = s[:-1]
    try:
        return float(s) * mult
    except:
        return None
