import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StructuralAnalysis", # Replace with your own username
    version="0.21",
    author="Hazem Kassab",
    author_email="Hazem_Kassab@hotmail.com",
    description="Package that performs structural analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=["StructuralAnalysis.", "StructuralAnalysis\\FrameElements"],
    include_package_data=True,
    install_requires=["numpy==1.19.5",
                      "PyOpenGL==3.1.5",
                      "PyQt5==5.15.2",
                      "pyqtgraph==0.11.1"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)