#!/usr/bin/env python3
import argparse, json
from modules.extractor import extract_slide_texts_and_images
from modules.normalizer import extract_numbers_and_dates
from modules.comparator import find_inconsistencies

def main():
    p = argparse.ArgumentParser()
    p.add_argument("pptx", help="Path to .pptx file")
    p.add_argument("--out", default="report.json", help="Output JSON file")
    p.add_argument("--use-ocr", action="store_true", help="Run OCR for images")
    p.add_argument("--llm", action="store_true", help="Use Gemini LLM for semantic checks")
    args = p.parse_args()

    slides = extract_slide_texts_and_images(args.pptx, use_ocr=args.use_ocr)
    facts = []
    for s in slides:
        facts_in_slide = extract_numbers_and_dates(s)
        for f in facts_in_slide:
            f['slide_index'] = s['index']
        facts.extend(facts_in_slide)

    report = {
        "summary": f"{len(find_inconsistencies(facts, slides, use_llm=args.llm))} potential inconsistencies found",
        "inconsistencies": find_inconsistencies(facts, slides, use_llm=args.llm)
    }

    with open(args.out, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"Report written to {args.out}")

if __name__ == "__main__":
    main()
