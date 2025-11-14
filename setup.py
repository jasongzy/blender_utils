import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blender_utils",
    version="1.1.0",
    author="jasongzy",
    author_email="jasongzy@gmail.com",
    description="blender_utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasongzy/blender_utils",
    project_urls={"Bug Tracker": "https://github.com/jasongzy/blender_utils/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["bu"],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "all": ["bpy", "fake-bpy-module"],
    },
)
