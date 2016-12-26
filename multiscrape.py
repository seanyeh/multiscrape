#!/usr/bin/env python3

import argparse
import os

from splinter import Browser


def run(url, css, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with Browser() as b:
        b.visit(url)

        links = [e["href"] for e in b.find_by_css(css)]

        for link in links:
            b.visit(link)

            # Create filename from last part of url
            filename = b.url[b.url.rfind("/") + 1:]
            if not filename.endswith(".html"):
                filename += ".html"

            filename = os.path.join(output_dir, filename)

            with open(filename, "w") as f:
                f.write(b.html)


def main():
    desc = '''
    A simple script to automate clicking on links and saving the webpages
    '''

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--url", "-u", type=str,
            required=True,
            help="URL to visit")
    parser.add_argument("--selector", "-s", type=str,
            required=True,
            help="CSS selector of links to visit and save")
    parser.add_argument("OUTPUT_DIR",
            nargs="?", default=".",
            help="Output directory. Default: Current directory")

    args = parser.parse_args()

    run(args.url, args.selector, args.OUTPUT_DIR)



if __name__ == "__main__":
    main()
