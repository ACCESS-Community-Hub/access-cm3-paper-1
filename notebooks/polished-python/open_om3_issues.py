#!/usr/bin/env python3
"""Open missing "Evaluation OM3: ..." issues on access-cm3-paper-1 and write the
GitHub Issue(s) cell of every OM3 notebook in notebooks/polished-python/mkfigs_issues.py.

Convention (one CM3 issue per OM3 issue):
  title  "Evaluation OM3: " + the OM3 issue title without its "Evaluation: " prefix
         (first letter capitalised, trailing "." dropped)
  body   the OM3 issue description (the @ of @-mentions dropped, so nobody is pinged), then
             Notebook: <access-om3-paper-1 notebook URL>      (one line per notebook)
             OM3 Issue: <access-om3-paper-1 issue URL>
  labels evaluation, CM3, OM3, polished-python
Landing-page cell, one line per CM3 issue (option B):
  **[CM3 #36: Mean sea surface temperature bias](...)** ([OM3 #9](...))

Which OM3 issues a notebook has comes from access-om3-paper-1's own
notebooks/mkfigs_issues.py (in the submodule), for the notebooks in the CM3
mkfigs.sh `om3_array`. For each OM3 issue the CM3 issue is one whose title
matches exactly or whose body links that OM3 issue, else it is opened (with
--create). Only open CM3 issues are linked; if several match (duplicates), the
one with the most comments wins (where the discussion is), then the lowest number.
If only closed CM3 issues match, the OM3 issue gets no CM3 link and none is opened. A notebook whose OM3 issues
share one CM3 issue gets one line: **[CM3 #67: ...]** ([OM3 #6], [OM3 #7]).

Usage, from notebooks/polished-python/ with the OM3 submodule checked out
(needs gh: module use /g/data/vk83/modules && module load gh):
    python3 open_om3_issues.py            # dry run: what it would open and write
    python3 open_om3_issues.py --create   # open the issues, then edit mkfigs_issues.py
Run it after adding a notebook to `om3_array` (or bumping the OM3 submodule).

Safe to re-run. mkfigs_issues.py is only edited, never committed.
"""
import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

CM3_REPO = "ACCESS-Community-Hub/access-cm3-paper-1"
OM3_REPO = "ACCESS-Community-Hub/access-om3-paper-1"
CM3_GH = f"https://github.com/{CM3_REPO}"
OM3_GH = f"https://github.com/{OM3_REPO}"
LABELS = ["evaluation", "CM3", "OM3", "polished-python"]
PREFIX = "Evaluation OM3: "

# OM3 issues that should not get a CM3 issue (not an evaluation figure).
EXCLUDE_OM3_ISSUES = {154}  # Truncation_locations: needs ocean.stats, which CM3 does not write

# OM3 issues tracked on an existing CM3 issue instead of their own one, e.g. both SSH
# plots (OM3 #4 mean, #5 standard deviation) are discussed on CM3 #80.
CM3_ISSUE_OVERRIDES = {5: 80}

# CM3 titles that differ from the rule, for OM3 issues whose title isn't a figure description.
TITLE_OVERRIDES = {
    154: PREFIX + "Velocity truncation locations",  # OM3: "Add truncation-location diagnostics to the evaluation workflow"
}


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def om3_array(cm3_repo):
    """Uncommented names in the CM3 mkfigs.sh om3_array."""
    s = (cm3_repo / "notebooks/polished-python/mkfigs.sh").read_text()
    block = re.search(r"^om3_array=\((.*?)^\)", s, re.S | re.M).group(1)
    return [l.split()[0] for l in block.splitlines() if l.strip() and not l.strip().startswith("#")]


def om3_issue_numbers(cm3_repo):
    """{notebook: [OM3 issue numbers]} from access-om3-paper-1's mkfigs_issues.py ISSUES."""
    src = (cm3_repo / "external/access-om3-paper-1/notebooks/mkfigs_issues.py").read_text()
    tree = ast.parse(src)
    for node in tree.body:
        target = getattr(node, "target", None) or (node.targets[0] if isinstance(node, ast.Assign) else None)
        if getattr(target, "id", None) == "ISSUES":
            out = {}
            for k, v in zip(node.value.keys, node.value.values):
                text = ast.unparse(v)
                # only access-om3-paper-1 issues ({_GH}/N), not e.g. access-om3-configs links
                out[k.value] = list(dict.fromkeys(int(n) for n in re.findall(r"\{_GH\}/(\d+)", text)))
            return out
    sys.exit("no ISSUES in access-om3-paper-1 mkfigs_issues.py")


def cm3_title(om3_title, om3_number=None):
    if om3_number in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[om3_number]
    t = re.sub(r"^\s*Evaluation:\s*", "", om3_title).strip().rstrip(".").strip()
    return PREFIX + t[:1].upper() + t[1:]


def strip_mentions(body):
    # OM3 issue-template boilerplate: keep only the description
    body = re.split(r"^#+\s*Check list", body, flags=re.M | re.I)[0]
    body = re.sub(r"^#+\s*Issue description\s*\n", "", body, flags=re.M | re.I)
    body = re.sub(r"^.*below is a set of tips for contributing.*\n?", "", body, flags=re.M)
    # sign-offs at the end of a line ("... Fig 27. @anton-seaice.") are dropped
    body = re.sub(r"(?:[ \t]+@[A-Za-z0-9-]+)+\.?[ \t]*$", "", body, flags=re.M)
    # other @-mentions keep the name without the "@", so GitHub will not notify them
    body = re.sub(r"(?<![\w/`])@(?=[A-Za-z0-9-])", "", body)
    return re.sub(r"[ \t]+\n", "\n", body).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cm3_repo", type=Path, nargs="?", default=Path(__file__).resolve().parents[2],
                    help="access-cm3-paper-1 checkout (default: the one this script is in)")
    ap.add_argument("--create", action="store_true", help="open the issues and edit mkfigs_issues.py (default: dry run)")
    a = ap.parse_args()
    issues_py = a.cm3_repo / "notebooks/polished-python/mkfigs_issues.py"

    notebooks = om3_array(a.cm3_repo)
    om3_map = om3_issue_numbers(a.cm3_repo)
    wanted = {nb: [n for n in om3_map.get(nb, []) if n not in EXCLUDE_OM3_ISSUES] for nb in notebooks}
    om3_numbers = sorted({n for ns in wanted.values() for n in ns})

    om3_info = {n: json.loads(gh("issue", "view", str(n), "-R", OM3_REPO, "--json", "title,body")) for n in om3_numbers}
    cm3_existing = json.loads(gh("issue", "list", "-R", CM3_REPO, "--state", "all", "--limit", "500",
                                 "--search", f'"{PREFIX.strip()}" in:title', "--json", "number,title,body,comments,state"))
    is_open = {i["number"]: i.get("state", "OPEN") == "OPEN" for i in cm3_existing}
    ncomments = {i["number"]: len(i.get("comments") or []) for i in cm3_existing}

    cm3_for = {}  # OM3 issue number -> CM3 issue number (None = would open)
    for n in om3_numbers:
        if n in CM3_ISSUE_OVERRIDES:
            cm3_for[n] = CM3_ISSUE_OVERRIDES[n]
            print(f"OM3 #{n:<4} -> CM3 #{cm3_for[n]} (override)")
            continue
        title = cm3_title(om3_info[n]["title"], n)
        by_title = sorted(i["number"] for i in cm3_existing if i["title"].strip() == title)
        by_link = sorted(i["number"] for i in cm3_existing
                         if re.search(rf"access-om3-paper-1/issues/{n}(?!\d)", i["body"] or ""))
        allc = set(by_title + by_link)
        cands = sorted((c for c in allc if is_open[c]), key=lambda c: (-ncomments[c], c))
        closed = sorted(c for c in allc if not is_open[c])
        found = cands[0] if cands else None
        if not found and closed:
            # a matching CM3 issue exists but was closed on purpose: don't link it, don't reopen a duplicate
            print(f"OM3 #{n:<4} -> only closed CM3 issue(s) {', '.join(f'#{c}' for c in closed)}: not linked, not opened")
            cm3_for[n] = "closed"
            continue
        if found:
            dupes = [f"#{d} ({ncomments[d]} comments)" for d in cands[1:]] + [f"#{d} (closed, not linked)" for d in closed]
            print(f"OM3 #{n:<4} -> CM3 #{found} ({ncomments[found]} comments){'  [duplicates: ' + ', '.join(dupes) + ']' if dupes else ''}")
            cm3_for[n] = found
            continue
        nbs = [nb for nb in notebooks if n in wanted[nb]]
        body = "\n".join([strip_mentions(om3_info[n]["body"] or ""), ""]
                         + [f"Notebook: {OM3_GH}/blob/main/notebooks/{nb}.ipynb" for nb in nbs]
                         + [f"OM3 Issue: {OM3_GH}/issues/{n}"])
        if not a.create:
            print(f"OM3 #{n:<4} -> WOULD OPEN: {title}\n    " + body.replace("\n", "\n    "))
            cm3_for[n] = None
            continue
        url = gh("issue", "create", "-R", CM3_REPO, "--title", title, "--body", body,
                 *[x for l in LABELS for x in ("--label", l)]).strip()
        cm3_for[n] = int(url.rstrip("/").rsplit("/", 1)[1])
        cm3_existing.append({"number": cm3_for[n], "title": title, "body": body})
        is_open[cm3_for[n]] = True; ncomments[cm3_for[n]] = 0
        print(f"OM3 #{n:<4} -> opened CM3 #{cm3_for[n]}: {title}  {url}")

    titles = {i["number"]: i["title"].strip() for i in cm3_existing}
    cells = {}
    for nb in notebooks:
        groups = {}  # CM3 issue (or ("new", OM3 n)) -> [OM3 numbers], in order
        for n in wanted[nb]:
            if cm3_for[n] == "closed":
                continue
            groups.setdefault(cm3_for[n] or ("new", n), []).append(n)
        lines = []
        for c, ns in groups.items():
            new = isinstance(c, tuple)
            full = cm3_title(om3_info[ns[0]]["title"], ns[0]) if new else titles[c]
            t = full[len(PREFIX):] if full.startswith(PREFIX) else full
            t = re.sub(r"^Evaluation:\s*", "", t)
            num = "#?" if new else f"#{c}"
            om3 = ", ".join(f"[OM3 #{n}]({{_OM3}}/{n})" for n in ns)
            lines.append(f"**[CM3 {num}: {t}]({{_GH}}/{'?' if new else c})** ({om3})")
        # notebooks with only excluded / no OM3 issues keep a bracketed OM3 link, if any
        if not lines and om3_map.get(nb):
            lines = [f"([OM3 #{n}]({{_OM3}}/{n}))" for n in om3_map[nb]]
        cells[nb] = "<br>".join(lines)

    print("\nGitHub Issue(s) cells:")
    for nb, cell in cells.items():
        print(f"  {nb}: {cell or '(none)'}")
    if not a.create:
        print("\nDry run: nothing opened, mkfigs_issues.py not changed. Re-run with --create.")
        return

    s = issues_py.read_text()
    if not re.search(r'^_OM3 = ', s, re.M):
        s = s.replace(f'_GH = "{CM3_GH}/issues"\n', f'_GH = "{CM3_GH}/issues"\n_OM3 = "{OM3_GH}/issues"\n', 1)
    for nb, cell in cells.items():
        if not cell:
            continue
        line = f'    {chr(34) + nb + chr(34) + ":":<42}f"{cell}",\n'
        pat = re.compile(rf'^    "{re.escape(nb)}":.*\n', re.M)
        s = pat.sub(lambda m: line, s, count=1) if pat.search(s) else s.replace("\n}\n", f"\n{line}}}\n", 1)
    issues_py.write_text(s)
    print(f"\nUpdated {issues_py} (not committed): git -C {a.cm3_repo} diff -- {issues_py.relative_to(a.cm3_repo)}")


if __name__ == "__main__":
    main()
