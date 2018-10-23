#! /usr/bin/env python

import argparse
from datetime import datetime
import md5
import os
import re
import sys


def get_title(md):
    match = re.search(r"#+ (.+)\n", md)
    if match:
        return match.groups()[0].strip()
    return "DAZ.ZONE"


def get_file_metadata(source_fp):
    with open(source_fp) as f:
        source = f.read()
    title = get_title(source)
    ctime = os.path.getctime(source_fp)
    basename, _ext = os.path.splitext(os.path.basename(source_fp))
    title_start = source.find(title)
    if title_start == -1:
        body_start = 0
    else:
        body_start = title_start + len(title)
    summary = " ".join(source[body_start:body_start + 140].strip().split()[:-1])
    return {
        "title": title,
        "ctime": datetime.fromtimestamp(ctime),
        "basename": basename,
        "md": source,
        "summary": "{}...".format(summary)
    }


def render(source, template):
    title = get_title(source)
    render_params = {"title": title, "md_src": source}
    html = template.format(**render_params)
    return html


def make_index(with_metadata, template):
    post_list = [
         "{ctime:%B %-d, %Y} - [{title}](/blog/{basename}.html)"
        .format(**info) for info in with_metadata
    ]

    index_md = "# DAZ.ZONE ARCHIVE\n\n{}\n".format("\n<br>\n".join(post_list))
    return render(index_md, template)


def make_feed(with_metadata, entry_template, feed_template):
    generated_time = "{:%Y-%m-%dT%H:%M:%S}".format(datetime.now())
    entries = [
        entry_template.format(md5=md5.md5(entry["title"]).hexdigest(), **entry)
        for entry in with_metadata
    ]
    feed = feed_template.format(
        generated_time=generated_time,
        entries="\n".join(entries)
    )
    return feed


def regenerate_all(src_dir, out_dir, post_template, feed_template, entry_template):
    if not os.path.isdir(src_dir):
        msg = "{} is not a directory!".format(os.path.abspath(src_dir))
        raise RuntimeError(msg)

    is_md = lambda f: os.path.isfile(os.path.abspath(f)) and os.path.splitext(f)[1] == ".md"

    dirname, _subdirs, files = os.walk(src_dir).next()  # no subdirs
    has_dir = [os.path.join(dirname, f) for f in files]
    src_paths = [f for f in has_dir if is_md(f)]
    with_metadata = sorted(
        [get_file_metadata(s) for s in src_paths],
        key=lambda i: i["ctime"],
        reverse=True
    )

    print("Found posts:\n\n{}\n".format("\n".join(i["basename"] for i in with_metadata)))
    index_html = make_index(with_metadata, post_template)
    index_path =os.path.join(out_dir, "index.html")
    print("Writing index to {}...".format(index_path))
    with open(index_path, "w") as f:
        f.write(index_html)

    atom_xml = make_feed(with_metadata, entry_template, feed_template)
    feed_path = os.path.join(out_dir, "feed", "atom_feed.xml")
    print("Writing feed to {}...".format(feed_path))
    with open(feed_path, "w") as f:
        f.write(atom_xml)
    for info in with_metadata:
            html = render(info["md"], post_template)

            out_file = os.path.join(out_dir, "{}.html".format(info["basename"]))
            print("Writing to {}...".format(out_file))
            with open(out_file, "w") as f:
                f.write(html)
    print("Done!")


def argparser():
    parser = argparse.ArgumentParser(description="Slot Markdown into some HTML.")
    parser.add_argument("-s", "--source", default="src/posts")
    parser.add_argument("--template", default="templates/post_template.html")
    parser.add_argument("-a", "--all", action="store_true")

    return parser


if __name__ == "__main__":
    parser = argparser()
    args = parser.parse_args()

    with open(args.template) as f:
        post_template = f.read()
    with open("templates/atom_feed.xml") as f:
        feed_template = f.read()
    with open("templates/atom_entry.xml") as f:
        entry_template = f.read()

    if args.all:
        regenerate_all(
            args.source,
            "blog",
            post_template,
            feed_template,
            entry_template
        )
    else:
        rendered = render(args.source, args.template)
        sys.stdout.write(rendered)
