#!/usr/bin/python


import pathlib
import re

def replace_top_items(text):
    stack = []
    out = []
    for line in text.splitlines(keepends=True):
        # detect begin/end environments
        m = re.match(r'\\begin\{(\w+)\}', line)
        if m:
            stack.append(m.group(1))
        m = re.match(r'\\end\{(\w+)\}', line)
        if m and stack and stack[-1] == m.group(1):
            stack.pop()

        # Replace only top-level \item
        if stack and stack[-1] in ("enumerate", "itemize") and len(stack) == 1:
            line = re.sub(
                r'\\item\b',
                r'\\end{exercise}\n\n\\begin{exercise}',
                line,
                count=1
            )
        out.append(line)
    return "".join(out)

for f in pathlib.Path(".").glob("*.tex"):
    text = f.read_text()
    new_text = replace_top_items(text)
    f.write_text(new_text)
    print(f"Processed {f}")
