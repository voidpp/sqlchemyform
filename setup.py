from setuptools import setup, find_packages

setup(
    name="Sqlchemyforms",
    version='0.1',
    install_requires=[
        "SQLAlchemy >= 0.9.8"
    ],
    packages=find_packages()
)

