"""Build the Balesin 2027 travel form pages from src/form.template.html.

Each conference date range gets its own fixed page, so members only ever see
their own dates. Run:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = (ROOT / "src" / "form.template.html").read_text()
ENDPOINT = "https://businessblueprint.awesomate.io/webhook/balesin-2027-travel-v3"

VERSIONS = [
    {"slug": "11-18-april", "dates": "11–18 April 2027", "arrival": "Sunday 11 April 2027"},
    {"slug": "18-25-april", "dates": "18–25 April 2027", "arrival": "Sunday 18 April 2027"},
]

# Live member pages (connected); preview pages never submit anything.
BUILD_LIVE = True


def render(v, endpoint, preview, base, tools=None, bar=""):
    out = TEMPLATE
    for token, value in {
        "__DATES_PLAIN__": v["dates"].replace("–", "-"),
        "__DATES__": v["dates"],
        "__ARRIVAL__": v["arrival"],
        "__ENDPOINT__": endpoint,
        "__PREVIEW__": "true" if preview else "false",
        "__TOOLS__": "true" if (preview if tools is None else tools) else "false",
        "__BARTEXT__": bar,
        "__BASE__": base,
    }.items():
        out = out.replace(token, value)
    for t in ("__DATES_PLAIN__", "__DATES__", "__ARRIVAL__", "__ENDPOINT__", "__PREVIEW__", "__TOOLS__", "__BARTEXT__", "__BASE__"):
        assert t not in out, t
    return out


for v in VERSIONS:
    p = ROOT / "preview" / v["slug"] / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(v, "", True, "../../", bar="Preview for review. Nothing entered here is submitted."))
    print("built", p.relative_to(ROOT))
    # Test links: really submit to n8n (sheet + Drive), for internal testing only.
    p = ROOT / "test" / v["slug"] / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(v, ENDPOINT, False, "../../", tools=True,
                        bar="TEST VERSION. Submissions are real and go to the sheet and Drive. Internal use only, do not send to members."))
    print("built", p.relative_to(ROOT))
    if BUILD_LIVE:
        p = ROOT / v["slug"] / "index.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render(v, ENDPOINT, False, "../"))
        print("built", p.relative_to(ROOT))
