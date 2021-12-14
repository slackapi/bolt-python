#!/usr/bin/env python
import os
import sys

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
exec(open(f"{here}/slack_bolt/version.py").read())

with open(f"{here}/README.md", "r") as fh:
    long_description = fh.read()

test_dependencies = [
    "pytest>=6.2.5,<7",
    "pytest-cov>=3,<4",
    "Flask-Sockets>=0.2,<1",
    "Werkzeug<2",  # TODO: support Flask 2.x
    "black==21.12b0",
]

async_test_dependencies = test_dependencies + [
    "pytest-asyncio<1",  # for async
    "aiohttp>=3,<4",  # for async
]

setuptools.setup(
    name="slack_bolt",
    version=__version__,
    license="MIT",
    author="Slack Technologies, LLC",
    author_email="opensource@slack.com",
    description="The Bolt Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slackapi/bolt-python",
    packages=setuptools.find_packages(
        exclude=[
            "examples",
            "integration_tests",
            "tests",
            "tests.*",
        ]
    ),
    include_package_data=True,  # MANIFEST.in
    install_requires=[
        "slack_sdk>=3.9.0,<4",
    ],
    setup_requires=["pytest-runner==5.2"],
    tests_require=async_test_dependencies,
    test_suite="tests",
    extras_require={
        # pip install -e ".[async]"
        "async": [
            # async features heavily depends on aiohttp
            "aiohttp>=3,<4",
            # Socket Mode 3rd party implementation
            "websockets>=8,<10",
        ],
        # pip install -e ".[adapter]"
        # NOTE: any of async ones requires pip install -e ".[async]" too
        "adapter": [
            # used only under src/slack_bolt/adapter
            "boto3<=2",
            # TODO: Upgrade to v2
            "moto<2",  # For AWS tests
            "bottle>=0.12,<1",
            "boddle>=0.2,<0.3",  # For Bottle app tests
            "chalice>=1.26.1,<2",
            "click>=7,<8",  # for chalice
            "CherryPy>=18,<19",
            "Django>=3,<4",
            "falcon>=2,<3",
            "fastapi>=0.70.0,<1",
            "Flask>=1,<2",
            "Werkzeug<2",  # TODO: support Flask 2.x
            "pyramid>=1,<2",
            "sanic>=21,<22" if sys.version_info.minor > 6 else "sanic>=20,<21",
            "sanic-testing>=0.7" if sys.version_info.minor > 6 else "",
            "starlette>=0.14,<1",
            "requests>=2,<3",  # For starlette's TestClient
            "tornado>=6,<7",
            # server
            "uvicorn<1",
            "gunicorn>=20,<21",
            # Socket Mode 3rd party implementation
            # TODO: 1.2.2 has a regression (https://github.com/websocket-client/websocket-client/issues/769)
            # ERROR on_error invoked (error: AttributeError, message: 'Dispatcher' object has no attribute 'read')
            "websocket_client>=1,<1.2.2",
        ],
        # pip install -e ".[testing_without_asyncio]"
        "testing_without_asyncio": test_dependencies,
        # pip install -e ".[testing]"
        "testing": async_test_dependencies,
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
