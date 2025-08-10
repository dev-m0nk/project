from collections import defaultdict                  # used defaultdict do if a ley doesnt exist it still dont give KeyError

def find_inconsistencies(facts, slides, use_llm=False):       # facts slide and a flag for llm as argument
    inconsistencies = []
    facts_by_type = defaultdict(list)                        # new dict

    for f in facts:
        facts_by_type[f["type"]].append(f)

    for t, items in facts_by_type.items():            #inserted in a set.If the set contain more than one value it flag and tells us that multiple data were found for same entry point
        seen_vals = {f["value"] for f in items if isinstance(f["value"], (int, float))}
        if len(seen_vals) > 1:    
            inconsistencies.append({
                "type": f"{t}_mismatch",
                "items": items,
                "explanation": f"Different {t} values detected in deck"
            })

    for slide in slides:
        total_hours = None
        component_hours = []
        for t in slide["texts"]:
            if "Hours Saved Per Consultant Monthly" in t:
                try:
                    total_hours = int([w for w in t.split() if w.isdigit()][0])
                except:
                    pass
            for w in t.split():
                if w.isdigit():
                    component_hours.append(int(w))
        if total_hours and sum(component_hours) - total_hours != total_hours:                # collect all component hours and total hours and check if there is a sum mismatch
            inconsistencies.append({
                "type": "sum_mismatch",
                "slide": slide["index"],
                "total": total_hours,
                "components_sum": sum(component_hours) - total_hours,
                "explanation": "Sum of components does not match total hours claimed"
            })

    return inconsistencies
