"""Narrow adaptation of the owner-supplied UCC required-sections primitive.

Source: CoherenceLattice f0566d8f79c308eaeb9ab10cb8255478e8913a71,
ucc/src/ucc/core.py::check_required_sections. See governed-core reuse record.
The original metrics/flags algorithm is retained. Text must actually be text;
str(None), booleans and objects cannot establish a completed section.
No donor file loader, research executor or arbitrary step registry is imported.
"""


def check_required_sections(input_doc, sections_key, required):
    sec=input_doc.get(sections_key,{})
    if type(sec) is not dict:raise ValueError('UCC_SECTION_OBJECT_REQUIRED')
    present={}
    for section in required:
        text=sec.get(section,'')
        present[section]=type(text) is str and bool(text.strip())
    missing=[section for section,ok in present.items() if not ok]
    present_count=sum(1 for ok in present.values() if ok)
    required_count=len(required)
    coverage=(present_count/required_count) if required_count else 0.0
    metrics={'required_sections':list(required),'present_sections':[section for section,ok in present.items() if ok],
        'missing_sections':missing,'section_coverage':coverage,'present_count':present_count,'required_count':required_count}
    flags={'sections_complete':len(missing)==0,'sections_missing':missing}
    return metrics,flags
