#!/usr/bin/env python3
"""Assemble index.html from template.html, content.md, and partials/.

content.md is the prose source. Supported constructs, one per block,
blocks separated by blank lines.

  {{name}}                 insert partials/name.html verbatim
  ## 4 Title {#anchor}     numbered section heading with anchor id
  @kick TEXT               the small uppercase label above a heading
  @status TEXT             the status line under a heading
  @kpis                    followed by "value :: label" lines
  @spec                    followed by "term :: definition" lines
  | a | b |                markdown table (second line is the ruler),
                           raw inline HTML allowed in cells
  anything else            a paragraph, **bold**, [text](url), `code`,
                           raw inline HTML and entities pass through

The paragraph starting with **Abstract.** receives id="abstract".
Figures, captions, the listing, and all SVG live in partials/ and are
edited there. Never edit index.html directly, it is generated.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def render_table(rows):
    def cells(row, tag):
        cs = [c.strip() for c in row.strip().strip("|").split("|")]
        return "".join(f"<{tag}>{c}</{tag}>" for c in cs)

    head = cells(rows[0], "th")
    body = "\n".join("        <tr>" + cells(r, "td") + "</tr>" for r in rows[2:])
    return (
        '  <div class="tabwrap">\n    <table>\n      <thead><tr>' + head
        + "</tr></thead>\n      <tbody>\n" + body
        + "\n      </tbody>\n    </table>\n  </div>"
    )


def render_line(line):
    m = re.match(r"^## (\d+) (.+?) \{#([a-z0-9-]+)\}$", line)
    if m:
        return (f'  <h2 id="{m.group(3)}"><span class="n">{m.group(1)}'
                f"</span>{m.group(2)}</h2>")
    if line.startswith("@kick "):
        return f'  <div class="kick">{line[6:]}</div>'
    if line.startswith("@status "):
        return f'  <p class="status"><b>Status</b> &nbsp;{inline(line[8:])}</p>'
    text = inline(line)
    pid = ' id="abstract"' if text.startswith("<strong>Abstract.</strong>") else ""
    return f"  <p{pid}>{text}</p>"


def render(md):
    out = []
    for group in md.strip("\n").split("\n\n"):
        lines = [l for l in group.split("\n") if l.strip()]
        parts = []
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("{{") and s.endswith("}}"):
                name = s[2:-2].strip()
                parts.append((ROOT / "partials" / f"{name}.html").read_text().rstrip("\n"))
                i += 1
            elif s == "@kpis":
                i += 1
                items = []
                while i < len(lines) and " :: " in lines[i]:
                    v, k = lines[i].split(" :: ", 1)
                    items.append((v.strip(), k.strip()))
                    i += 1
                rows = "\n".join(
                    f'    <div class="kpi"><div class="v">{v}</div>'
                    f'<div class="k">{k}</div></div>' for v, k in items)
                parts.append('  <div class="kpis">\n' + rows + "\n  </div>")
            elif s == "@spec":
                i += 1
                pairs = []
                while i < len(lines) and " :: " in lines[i]:
                    t, d = lines[i].split(" :: ", 1)
                    pairs.append((t.strip(), inline(d.strip())))
                    i += 1
                body = "\n\n".join(
                    f"    <dt>{t}</dt>\n    <dd>{d}</dd>" for t, d in pairs)
                parts.append('  <dl class="spec">\n' + body + "\n  </dl>")
            elif s.startswith("|"):
                tbl = []
                while i < len(lines) and lines[i].startswith("|"):
                    tbl.append(lines[i])
                    i += 1
                parts.append(render_table(tbl))
            else:
                parts.append(render_line(lines[i]))
                i += 1
        out.append("\n".join(parts))
    return "\n\n".join(out)


def main():
    tpl = (ROOT / "template.html").read_text()
    content = render((ROOT / "content.md").read_text())
    html = tpl.replace("{{content}}", content)
    (ROOT / "index.html").write_text(html)
    print(f"wrote index.html ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
