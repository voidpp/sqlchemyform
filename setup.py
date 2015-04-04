from setuptools import setup, find_packages

setup(
    name = "Sqlchemyforms",
    description = "Generate form objects for create HTML forms based on SQLAlchhemy models",
    version = '1.0',
    install_requires = [
        "SQLAlchemy >= 0.9.8",
    ],
    packages = find_packages()
)

