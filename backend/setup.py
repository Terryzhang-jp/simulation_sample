from setuptools import setup, find_packages

setup(
    name="simulation_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "numpy",
        "scipy",
        "pandas",
        "python-multipart",
        "plotly",
        "kaleido",
        "python-jose",
    ],
) 