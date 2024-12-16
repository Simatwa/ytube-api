from setuptools import setup

from setuptools import find_packages

INSTALL_REQUIRE = [
    "cloudscraper>=1.2.71",
    "tqdm==4.66.3",
]

cli_reqs = [
    "click==8.1.3",
    "rich==13.9.2",
    "prompt-toolkit==3.0.48",
    "colorama==0.4.6",
]

EXTRA_REQUIRE = {
    "cli": cli_reqs,
    "all": cli_reqs + [],
}

setup(
    name="ytube-api",
    version="0.1.0",
    license="MIT",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="Unofficial wrapper for y2mate.tube",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/Simatwa/ytube-api",
    project_urls={
        "Bug Report": "https://github.com/Simatwa/ytube-api/issues/new",
        "Homepage": "https://github.com/Simatwa/ytube-api",
        "Source Code": "https://github.com/Simatwa/ytube-api",
        "Issue Tracker": "https://github.com/Simatwa/ytube-api/issues",
        "Download": "https://github.com/Simatwa/ytube-api/releases",
        "Documentation": "https://github.com/Simatwa/ytube-api/",
    },
    entry_points={
        "console_scripts": [
            "ytube = ytube_api.console:main",
        ],
    },
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    python_requires=">=3.9",
    keywords=[
        "ytube",
        "ytube-api",
        "y2mate",
        "y2mate-api",
        "youtube",
        "ytdlp",
        "youtube-video-downloader",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
