from setuptools import setup, find_packages

setup(
    name="suture_ci",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "docker",
        "ollama",
        "PyGithub",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "suture-ci=main:start",
        ],
    },
    author="KSrikzz",
    description="An autonomous self-healing CI agent using local LLMs.",
    python_requires=">=3.9",
)