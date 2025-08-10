#!/usr/bin/env python3
import argparse, json                                                     #argparse to parse command line
from modules.extractor import extract_slide_texts_and_images              # function import from modules/extractor.py
from modules.normalizer import extract_numbers_and_dates                  # function import from modules/normalizer.py
from modules.comparator import find_inconsistencies                       # function import from modules/comparator.py



def main():                                                                # -> main function
    p = argparse.ArgumentParser()                                          # new parser object initiated
    p.add_argument("pptx", help="Path to .pptx file")                        # to detect ppt file
    p.add_argument("--out", default="report.json", help="Output JSON file")            # default json file for output
    p.add_argument("--use-ocr", action="store_true", help="Run OCR for images")            # Added ocr for text in image,graphs  
    p.add_argument("--llm", action="store_true", help="Use Gemini LLM for semantic checks") # Added gemini llm to get our response
    args = p.parse_args()                                                                   # parse the argument now

    slides = extract_slide_texts_and_images(args.pptx, use_ocr=args.use_ocr)                #this function is in extractor.py .. pptx file and ocr flag is passed as argument
    facts = []
    for s in slides:
        facts_in_slide = extract_numbers_and_dates(s)                    # extract slide data like numbers date, digits,currencies
        for f in facts_in_slide:                                          
            f['slide_index'] = s['index']                                  # I used it to mark slide number on each fact so it can be ofund easily
        facts.extend(facts_in_slide)

    report = {
        "summary": f"{len(find_inconsistencies(facts, slides, use_llm=args.llm))} potential inconsistencies found",                  # from comparator.py 
        "inconsistencies": find_inconsistencies(facts, slides, use_llm=args.llm)                        
    }

    with open(args.out, "w") as fh:                                    
        json.dump(report, fh, indent=2)                # Report writing in JSON
    print(f"Report written to {args.out}")               # Finished the report

if __name__ == "__main__":                                    # Direct execution from terminal and assigned main()
    main()
