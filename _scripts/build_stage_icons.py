"""Build v12 folder icons from the REAL Theophysics glyph artwork.
Composites each stage's glyph PNG onto a branch-colored tile with a
state dot. Replaces the Unicode-fallback icons.
Usage: python _scripts/build_stage_icons.py
"""
import os
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLYPHS = (r"C:\theophysics\00_Canonical_PRODUCTION_v1.0"
          r"\theophysics_glyphs_first_pass\theophysics_glyphs\png")
OUT = os.path.join(REPO, "_icons")

# v12 stage -> real glyph filename, branch
STAGES = [
    ("00_inbox_working",       "draft",           "cap"),
    ("01_middle_seed",         "binder",          "cap"),
    ("02_claim_atoms",         "claim",           "cap"),
    ("10_technical_canon",     "canonical",       "tech"),
    ("11_technical_paradigm",  "broken-symmetry", "tech"),
    ("12_technical_synthesis", "isomorphism",     "tech"),
    ("13_hypothesis",          "prediction",      "tech"),
    ("14_evidence",            "evidence",        "tech"),
    ("15_falsification",       "kill-condition",  "tech"),
    ("16_objections",          "doubt",           "tech"),
    ("17_doctoral_paper",      "proof",           "tech"),
    ("20_everyday_canon",      "truth",           "pub"),
    ("21_everyday_paradigm",   "consciousness",   "pub"),
    ("22_lived_synthesis",     "mesh",            "pub"),
    ("23_public_evidence",     "witness",         "pub"),
    ("24_application",         "sanctification",  "pub"),
    ("25_worldcheck",          "seven-question",  "pub"),
    ("26_audience",            "logos",           "pub"),
    ("30_real_world_verdict",  "justice",         "ver"),
    ("31_revision_return",     "repentance",      "ver"),
]

BAND = {"cap": (91, 107, 122), "tech": (46, 111, 183),
        "pub": (200, 134, 43), "ver": (107, 78, 155)}
DOT = {"empty": (120, 120, 120), "working": (240, 176, 50),
       "done": (60, 175, 95), "failed": (210, 60, 60)}


S = 256

def tile(glyph_png, branch, state):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base = BAND[branch]
    if state == "empty":
        base = tuple(int(c * 0.40 + 78) for c in base)
    d.rounded_rectangle((8, 8, S - 8, S - 8), radius=44, fill=base + (255,))

    g = Image.open(glyph_png).convert("RGBA")
    g = g.resize((160, 160), Image.LANCZOS)

    # glyph art is dark-on-transparent; recolor to white so it reads on the tile
    px = g.load()
    for y in range(g.height):
        for x in range(g.width):
            r, gr, b, a = px[x, y]
            if a > 0:
                v = 255 if state != "empty" else 235
                px[x, y] = (v, v, v, a if state != "empty" else int(a * 0.45))

    im.alpha_composite(g, ((S - 160) // 2, (S - 160) // 2 - 8))

    d.ellipse((S - 84, S - 84, S - 20, S - 20), fill=(28, 28, 28, 235))
    d.ellipse((S - 78, S - 78, S - 26, S - 26), fill=DOT[state] + (255,))
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    made = missing = 0
    for stage, glyph, branch in STAGES:
        src = os.path.join(GLYPHS, glyph + ".png")
        if not os.path.exists(src):
            print(f"  MISSING glyph: {glyph}.png  (for {stage})")
            missing += 1
            continue
        for state in DOT:
            tile(src, branch, state).save(
                os.path.join(OUT, f"{stage}__{state}.ico"),
                format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
            made += 1
    print(f"built {made} icons from real glyph artwork, {missing} glyphs missing")
    print("now run: python _scripts/set_folder_icons.py")
