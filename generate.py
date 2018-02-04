#! /usr/bin/env python

import argparse
import re
import sys

def read_source(filepath):
    with open(filepath) as f:
        source = f.read()
    return source


def render(source_fp, template_fp):
    with open(source_fp) as f:
        source = f.read()
    with open(template_fp) as f:
        template = f.read()
    match = re.search(r"#+ .+\n", source)
    if match:
        title = match[0].strip()
    else:
        title = "DAZ.ZONE"
    render_params = {"title": title, "md_src": source}
    html = template.format(**render_params)
    return html


def argparser():
    parser = argparse.ArgumentParser(description="Slot Markdown into some HTML.")
    parser.add_argument("source")
    parser.add_argument("--template", default="blog_template.html")

    return parser


if __name__ == "__main__":
    parser = argparser()
    args = parser.parse_args()
    rendered = render(args.source, args.template)
    sys.stdout.write(rendered)
