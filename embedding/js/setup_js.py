#!/usr/bin/env python
import subprocess
import argparse

output_template = """
(function (window, undefined) {

%(source_js)s

window.GLmol = GLmol;

}(window));
"""

def do_setup(beautify):
    """docstring for do_setup"""
    target_files = ["three.js", "GLmol.js"]

    cmd = ["uglifyjs"] + (["-b", "indent-level=4"] if beautify else []) + target_files

    source_js = subprocess.check_output(cmd)

    print output_template % dict(source_js = source_js)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup GLmol and THREE minified javascript.')
    parser.add_argument('--beautify', "-b", action="store_true", default=False, help='Produce beautified output js.')
    args = parser.parse_args()

    do_setup(**vars(args))
