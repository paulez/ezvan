#!/usr/bin/python3

from argparse import ArgumentParser, FileType
import re

def convert(file):
    with open(file, "r") as md_file:
        md_content = md_file.readlines()
    print("File line count: {}".format(len(md_content)))
    tags = []
    new_content = []
    for md_line in md_content:
        tag_match = re.search(
            "\[(.*)\]\(.*/taxonomy/term/.*\)",
            md_line)
        if tag_match:
            tags.append(tag_match.group(1))
        elif not filter_line(md_line):
            new_content.append(md_line)
    md_content = new_content
    new_content = []
    # add list of tags
    added = False
    for md_line in md_content:
        if not added and "Slug:" in md_line:
            added = True
            new_content.append("Tags: {}\n".format(
                ', '.join(tags)
            ))
        new_content.append(md_line)
    new_content = "".join(new_content)
    # remove multiline div tags
    new_content = re.sub(
        "<div[^>]*>\n",
        "",
        new_content,
        flags=re.DOTALL)
    # remove multiple blank lines
    new_content = re.sub(r'\n\s*\n', '\n\n', new_content)
    with open("{}.new".format(file), "w") as md_output:
        md_output.write(new_content)

def filter_line(line):
    """
    Filter non needed lines
    """
    if re.fullmatch("</p>\n", line):
        return True
    if re.fullmatch("<p>\n", line):
        return True
    if re.fullmatch("<div.*>\n", line):
        return True
    if re.fullmatch("</div>\n", line):
        return True
    if re.fullmatch("Thème:.*\n", line):
        return True
    return False

parser = ArgumentParser()
parser.add_argument('file', nargs="+")
args = parser.parse_args()

for file in args.file:
    convert(file)