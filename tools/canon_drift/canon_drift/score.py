from difflib import SequenceMatcher

from .normalize import equation_shape, normalize_equation


def score_candidate(text, retired, context, rules):
    norm = normalize_equation(text)
    target = normalize_equation(retired["pattern"])
    exact = text.strip() == retired["pattern"]
    normalized = norm == target
    ratio = SequenceMatcher(None, norm, target).ratio()
    a, b = equation_shape(text), equation_shape(retired["pattern"])
    structure = 0.0
    structure += .35 if a["lhs"] == b["lhs"] else 0
    structure += .30 if a["operator"] == b["operator"] else 0
    structure += .20 if a["derivative"] == b["derivative"] else 0
    structure += .15 * (len(set(a["variables"]) & set(b["variables"])) / max(1, len(set(b["variables"]))))
    confidence = 1.0 if exact else .97 if normalized else round(.55 * ratio + .35 * structure + .1, 2)
    protected = context in set(retired.get("allowedContexts", [])) or context in {"raw_fragment", "story"}
    safe = retired.get("safeAutoFix", False) and not protected
    if confidence >= rules["autoFixThreshold"] and safe:
        action, ruling = "auto_fix", False
    elif confidence >= rules["proposalThreshold"]:
        action, ruling = "propose_patch", True
    elif confidence >= rules["flagThreshold"]:
        action, ruling = "flag_only", True
    else:
        action, ruling = "ignore", False
    if protected and action == "auto_fix": action, ruling = "flag_only", True
    return {"confidence": confidence, "distance": round((1-confidence)*100), "action": action,
            "ruling": ruling, "protected": protected,
            "reason": "exact registry match" if exact else "normalized symbol match" if normalized else "equation structure and string similarity"}
