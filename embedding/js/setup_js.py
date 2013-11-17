#!/usr/bin/env python
import logging; logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")

import subprocess
import argparse

output_template = """
(function (window, undefined) {

%(source_js)s

window.GLmol = GLmol;

}(window));
"""

def do_setup(beautify, target_files):
    """docstring for do_setup"""
    logging.info("do_setup(%r)", locals())

    cmd = ["uglifyjs"] + (["-b", "indent-level=4"] if beautify else []) + target_files

    source_js = subprocess.check_output(cmd)

    print output_template % dict(source_js = source_js)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup minified javascript.')
    parser.add_argument('--beautify', "-b", action="store_true", default=False, help='Produce beautified output js.')
    parser.add_argument('target_files', type=str, nargs="*", default=["GLmol.js"], help="Included files")
    args = parser.parse_args()

    do_setup(**vars(args))
