from setuptools import setup

import re

with open("aio_piston/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name         = "aio_piston", 
    author       = "Tom-the-Bomb", 
    version      = version, 
    description  = "An unoffical async API wrapper for the piston code execution engine",
    long_description              = open("README.md").read(),
    long_description_content_type = "text/markdown",
    license      = "MIT",
    url          = "https://github.com/Tom-the-Bomb/aio-piston",
    project_urls = {
        "Repository"   : "https://github.com/Tom-the-Bomb/aio-piston",
        "Issue tracker": "https://github.com/Tom-the-Bomb/aio-piston/issues",
    },
    classifiers  = [
        "Intended Audience :: Developers",
        'Programming Language :: Python',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    include_package_data = True,
    packages             = ['aio_piston'],
    install_requires     = ['aiohttp'],
    zip_safe        = True,
    python_requires = '>=3.7'
)