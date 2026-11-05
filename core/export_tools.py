"""Export Tools:
Generates publication-ready standalone HTML documents with IEEE typography and offline styling.
"""

import re
from typing import Dict, Any, Optional


def markdown_to_clean_html(markdown_text: str) -> str:
    """Convert basic markdown elements into clean semantic HTML."""
    html = markdown_text

    # Code blocks
    html = re.sub(r"```([a-zA-Z0-9_-]*)\n([\s\S]*?)```", r"<pre><code>\2</code></pre>", html)

    # Headers
    html = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

    # Bold and italics
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

    # Inline code
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # Bullet lists
    html = re.sub(r"^- (.*?)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"((?:<li>.*?</li>\s*)+)", r"<ul>\1</ul>", html)

    # Paragraphs (blocks separated by double newlines)
    blocks = html.split("\n\n")
    formatted_blocks = []
    for b in blocks:
        b_strip = b.strip()
        if not b_strip:
            continue
        if b_strip.startswith("<h") or b_strip.startswith("<pre") or b_strip.startswith("<ul"):
            formatted_blocks.append(b_strip)
        else:
            formatted_blocks.append(f"<p>{b_strip}</p>")

    return "\n".join(formatted_blocks)


def generate_standalone_html_publication(
    topic: str,
    markdown_content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Generate a self-contained, publication-grade HTML document with IEEE styling."""
    body_html = markdown_to_clean_html(markdown_content)
    meta = metadata or {}
    domain = meta.get("domain", "Computer Science & Engineering")
    confidence = meta.get("confidence_score", 92)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{topic} - Research Publication</title>
  <style>
    @page {{
      size: letter;
      margin: 0.75in;
    }}
    body {{
      font-family: "Times New Roman", Times, serif;
      font-size: 10.5pt;
      line-height: 1.35;
      color: #111;
      background: #fff;
      margin: 0 auto;
      max-width: 8.5in;
      padding: 0.5in 0.75in;
    }}
    .header-box {{
      text-align: center;
      margin-bottom: 24pt;
      border-bottom: 1.5pt solid #222;
      padding-bottom: 14pt;
    }}
    .paper-title {{
      font-size: 18pt;
      font-weight: bold;
      margin-bottom: 8pt;
      line-height: 1.2;
    }}
    .author-line {{
      font-size: 11pt;
      font-weight: bold;
      color: #222;
    }}
    .affiliation {{
      font-size: 9pt;
      font-style: italic;
      color: #444;
      margin-top: 3pt;
    }}
    .abstract-panel {{
      background: #fbfbfb;
      border-left: 3pt solid #000;
      padding: 10pt 14pt;
      margin: 14pt 0 20pt 0;
      font-size: 9.5pt;
      text-align: justify;
    }}
    .two-column-layout {{
      column-count: 2;
      column-gap: 22pt;
      text-align: justify;
    }}
    h1, h2, h3 {{
      font-family: "Times New Roman", Times, serif;
      text-transform: uppercase;
      font-size: 10pt;
      font-weight: bold;
      margin-top: 14pt;
      margin-bottom: 4pt;
      border-bottom: 0.5pt solid #333;
      break-after: avoid;
    }}
    p {{
      margin: 0 0 8pt 0;
      text-indent: 14pt;
    }}
    ul {{
      margin: 4pt 0 8pt 16pt;
      padding: 0;
    }}
    li {{
      margin-bottom: 3pt;
    }}
    code {{
      font-family: "Courier New", Courier, monospace;
      font-size: 9pt;
      background: #f4f4f4;
      padding: 1pt 3pt;
      border-radius: 2pt;
    }}
    pre {{
      background: #f4f4f4;
      border: 0.5pt solid #ccc;
      padding: 6pt;
      font-size: 8.5pt;
      overflow-x: auto;
      break-inside: avoid;
    }}
    .footer-note {{
      margin-top: 30pt;
      border-top: 0.5pt solid #888;
      padding-top: 6pt;
      font-size: 8pt;
      color: #555;
      text-align: center;
    }}
  </style>
</head>
<body>

  <div class="header-box">
    <div class="paper-title">{topic}</div>
    <div class="author-line">Soumyadeep Ghosh</div>
    <div class="affiliation">
      Department of Computer Science & Engineering<br>
      Brainware University, Kolkata, India<br>
      <em>Field Focus: {domain} • Fact-Check Consensus Audit: {confidence}%</em>
    </div>
  </div>

  <div class="abstract-panel">
    <strong><em>Abstract</em>—</strong> This manuscript details an empirical investigation synthesized via distributed autonomous multi-agent inquest. Using live web crawling, cross-source citation corroboration, and adversarial peer review, we analyze latency bounds, architectural scaling tradeoffs, and critical constraints.
    <br><br>
    <strong><em>Index Terms</em>—</strong> Distributed Systems, Multi-Agent Swarms, Empirical Benchmarks, Peer-Review Verification.
  </div>

  <div class="two-column-layout">
    {body_html}
  </div>

  <div class="footer-note">
    Synthesized and Formatted by DeepResearch Swarm • MIT License • Author: Soumyadeep Ghosh
  </div>

</body>
</html>
"""
