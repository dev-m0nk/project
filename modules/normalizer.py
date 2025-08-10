import re                    # library for regular expression

def extract_numbers_and_dates(slide_data):
    facts = []
    all_texts = slide_data["texts"] + [img["ocr_text"] for img in slide_data["images"] if img["ocr_text"]] + [slide_data["notes"]]

    for text in all_texts:
        if not text:
            continue

        for m in re.finditer(r"\$?\d[\d,]*(?:\.\d+)?\s?(M|B|K)?", text):   # to find regular expression block
            raw = m.group()
            val = normalize_currency(raw)
            facts.append({"type": "currency", "value": val, "raw": raw, "context": text})

        for m in re.finditer(r"\d+(\.\d+)?\s?%", text):
            facts.append({"type": "percent", "value": float(m.group().replace("%", "")), "raw": m.group(), "context": text})   # find percentage and convert into float

        for m in re.finditer(r"\d+\s?(mins?|hours?|hrs?)", text, re.I):
            facts.append({"type": "duration", "value": m.group(), "raw": m.group(), "context": text})      # to find durations like mins hr sec

        for m in re.finditer(r"\d+x", text, re.I):
            facts.append({"type": "multiplier", "value": m.group(), "raw": m.group(), "context": text})   # to find multipliers

    return facts

def normalize_currency(raw):     # convert short form like M (million) to 1000000 etc
    s = raw.replace("$", "").replace(",", "").strip()
    mult = 1
    if s.lower().endswith("m"):           # M -> 1000000 (million)
        mult = 1_000_000
        s = s[:-1]
    elif s.lower().endswith("b"):         # B -> 1000000000 (billion)
        mult = 1_000_000_000
        s = s[:-1]
    elif s.lower().endswith("k"):         # K -> 1000 (thousand0
        mult = 1_000
        s = s[:-1]
    try:
        return float(s) * mult
    except:
        return None
