import setuptools

setuptools.setup(
    name="pb",
    version="1.0.0",
    description="Popbumper - A command line client",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    python_requires="~=3.8",
    install_requires=[
        "pyyaml >= 5.3, < 5.4.0a0",
        "requests >= 2.24, < 2.25.0a0",
        "tabulate >= 0.8.7, < 0.8.8a0",
    ],
    extras_require=dict(
        dev=["pre-commit", "ipdb", "flake8", "flake8-black"],
        test=["pytest", "pytest-cov"],
    ),
    entry_points=dict(console_scripts=["pb = pb.__main__:main"]),
)