#! /usr/bin/env python

import argparse
from datetime import datetime
import os
import re
import sys

def read_source(filepath):
    with open(filepath) as f:
        source = f.read()
    return source


def get_title(md):
    match = re.search(r"#+ (.+)\n", md)
    if match:
        return match.groups()[0].strip()
    return "DAZ.ZONE"


def get_info(source_fp):
    with open(source_fp) as f:
        source = f.read()
    title = get_title(source)
    mtime = os.path.getmtime(source_fp)
    basename, _ext = os.path.splitext(os.path.basename(source_fp))
    return {
        "title": title,
        "mtime": datetime.fromtimestamp(mtime),
        "basename": basename,
        "md": source
    }


def render(source, template):
    title = get_title(source)
    render_params = {"title": title, "md_src": source}
    html = template.format(**render_params)
    return html


def make_index(infos, template):
    post_list = [
         "{mtime:%B %-d, %Y} - [{title}](/blog/{basename}.html)"
        .format(**info) for info in infos
    ]

    index_md = "# DAZ.ZONE ARCHIVE\n\n{}\n".format("\n".join(post_list))
    return render(index_md, template)


def make_feed(infos):
    return "ah"


def regenerate_all(src_dir="src/posts", out_dir="blog", template_fp="template.html"):
    if not os.path.isdir(src_dir):
        msg = "{} is not a directory!".format(os.path.abspath(src_dir))
        raise RuntimeError(msg)

    with open(template_fp) as f:
        template = f.read()

    is_md = lambda f: os.path.isfile(os.path.abspath(f)) and os.path.splitext(f)[1] == ".md"

    dirname, _subdirs, files = os.walk(src_dir).next()  # no subdirs
    has_dir = [os.path.join(dirname, f) for f in files]
    srcs = [f for f in has_dir if is_md(f)]
    infos = sorted([get_info(s) for s in srcs], key=lambda i: i["mtime"])

    index_html = make_index(infos, template)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(index_html)

    atom_xml = make_feed(infos)
    with open(os.path.join(out_dir, "atom-feed.xml"), "w") as f:
        f.write(atom_xml)

    for info in infos:
        html = render(info["md"], template)

        out_file = os.path.join(out_dir, "{}.html".format(info["basename"]))
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
