#!/usr/bin/env python3

import os
import re

from setuptools import setup

init_path = os.path.join(os.path.dirname(__file__),
                         "radicale_imap", "__init__.py")
with open(init_path) as f:
    version = re.search(r'VERSION = "([^"]+)"', f.read()).group(1)

setup(
    name="Radicale_IMAP",
    version=version,
    description="IMAP authentication plugin for Radicale",
    author="Unrud",
    author_email="unrud@openaliasbox.org",
    url="http://github.com/Unrud/RadicaleIMAP",
    license="GNU GPL v3",
    platforms="Any",
    packages=["radicale_imap"])
