from setuptools import setup, find_packages

setup(
    name="azure_blob_uploader",
    version="1.0.0",
    description="A Python module to upload files to Azure Blob Storage with paths",
    author="Steve Gall",
    author_email="steve.gall@builder.ai",
    url="https://gitlab-internal.builder.ai/devsecops/tools/backup_azure_storage_container.git",
    packages=find_packages(),
    install_requires=[
        "azure-storage-blob>=12.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)