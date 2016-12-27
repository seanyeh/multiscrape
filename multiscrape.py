#!/usr/bin/env python3

import argparse
import logging
import os
import time

from splinter import Browser


def run(args):
    css = args.selector

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    with Browser() as b:
        links = []

        b.visit(args.url)

        # Loop to continuously go to "next" page
        while True:
            logging.info("Finding links")
            # Find all links
            links += [e["href"] for e in b.find_by_css(css)]

            logging.info("Done finding links")
            # Continue if no "next" css specified
            if not args.next_css:
                break

            next_link = b.find_by_css(args.next_css)
            logging.info("next links found: %d" % len(next_link))

            # Continue if no "next" link found
            if len(next_link) == 0:
                break

            # Loop again
            next_link[0].click()

            time.sleep(5) # For javascript next links


        for link in links:
            if not args.no_save:
                b.visit(link)

                if args.save_as_title:
                    filename = b.title
                else:
                    # Create filename from last part of url
                    filename = b.url[b.url.rfind("/") + 1:]
                    if not filename.endswith(".html"):
                        filename += ".html"

                filename = os.path.join(args.output_dir, filename)

                with open(filename, "w") as f:
                    f.write(b.html)

            # Print link
            print(link)


def main():
    desc = '''
    A simple script to automate clicking on links and saving the webpages
    '''

    parser = argparse.ArgumentParser(description=desc)

    # Required arguments
    parser.add_argument("--url", "-u", type=str,
            required=True,
            help="URL to visit")
    parser.add_argument("--selector", "-s", type=str,
            required=True,
            help="CSS selector of links to visit and save")

    # Additional options
    parser.add_argument("--no-save", "-ns", action="store_true",
            help="Don't save any webpages")
    parser.add_argument("--save-as-title", "-st", action="store_true",
            help="Use webpage title as filename for saved webpages")
    parser.add_argument("--next-css", "-n", type=str, default=None,
            help="CSS selector of \"Next\" page to continually click on")

    # Output
    parser.add_argument("output_dir", metavar="OUTPUT_DIR",
            nargs="?", default=".",
            help="Output directory. Default: Current directory")

    # Debug
    parser.add_argument("--debug", action="store_true",
            help="Show debug information")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.INFO)

    logging.info(args)

    run(args)



if __name__ == "__main__":
    main()
