#! /usr/bin/env python

import argparse
import os
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
    match = re.search(r"#+ (.+)\n", source)
    if match:
        title = match.groups()[0].strip()
    else:
        title = "DAZ.ZONE"
    render_params = {"title": title, "md_src": source}
    html = template.format(**render_params)
    return html


def regenerate_all(src_dir="src", out_dir="blog", template="template.html"):
    src_dir = "src"
    out_dir = "blog"
    if not os.path.isdir(src_dir):
        msg = "{} is not a directory!".format(os.path.abspath(src_dir))
        raise RuntimeError(msg)

    is_md = lambda f: os.path.isfile(os.path.abspath(f)) and os.path.splitext(f)[1] == ".md"

    dirname, _subdirs, files = os.walk(src_dir).next()  # no subdirs
    has_dir = [os.path.join(dirname, f) for f in files]
    srcs = [f for f in has_dir if is_md(f)]

    for src in srcs:
        basename, _ext = os.path.splitext(os.path.basename(src))
        out_file = os.path.join(out_dir, "{}.html".format(basename))
        html = render(src, template)
        print("Writing to {}...".format(out_file))
        with open(out_file, "w") as f:
            f.write(html)
    print("Done!")


def argparser():
    parser = argparse.ArgumentParser(description="Slot Markdown into some HTML.")
    parser.add_argument("-s", "--source")
    parser.add_argument("--template", default="template.html")
    parser.add_argument("-a", "--all", action="store_true")

    return parser


if __name__ == "__main__":
    parser = argparser()
    args = parser.parse_args()
    if args.all:
        regenerate_all()
    else:
        rendered = render(args.source, args.template)
        sys.stdout.write(rendered)
