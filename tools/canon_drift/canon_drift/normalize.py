import html
import re
import unicodedata


REPLACEMENTS = {
    "χ": "chi", "η": "eta", "Γ": "Gamma", "γ": "Gamma",
    "∏": "product", "∇": "grad", "×": "*", "−": "-",
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "₀": "_0", "₁": "_1", "ᵢ": "_i",
}


def normalize_equation(value):
    value = html.unescape(value)
    for old, new in REPLACEMENTS.items():
        value = value.replace(old, new)
    value = re.sub(r"\\(chi|eta|Gamma|prod|nabla)\b", lambda m: {"prod":"product", "nabla":"grad"}.get(m.group(1), m.group(1)), value)
    value = value.replace("$$", "").replace("$", "").replace("\\[", "").replace("\\]", "")
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\bprod(?:uct)?\b", "product", value, flags=re.I)
    return re.sub(r"\s+", "", value).lower()


def equation_shape(value):
    norm = normalize_equation(value)
    lhs, _, rhs = norm.partition("=")
    if "/" in rhs: operator = "ratio"
    elif "product" in rhs or "*" in rhs: operator = "product"
    elif "+" in rhs or "-" in rhs: operator = "sum"
    elif "l(" in norm or "lagrang" in norm: operator = "field"
    else: operator = "other"
    variables = sorted(set(re.findall(r"(?<![a-z])([gmes tkqrf])(?=[,)+*/\]-]|$)", norm.replace(" ", ""))))
    return {"lhs": lhs, "operator": operator, "variables": variables,
            "derivative": lhs.startswith("d") and "/d" in lhs,
            "wrapper": "c_w" in rhs or "cw[" in rhs}


MOJIBAKE = re.compile(r"(?:Ã.|Â.|â€|â€™|ï»¿|�)")
# Broad enough for maintenance reporting while excluding ordinary mathematical symbols.
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]")
