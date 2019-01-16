from setuptools import setup, find_packages

setup(
    name='syncwerk-server-python-rpc-bindings',
    version='20181227',
    author='Syncwerk GmbH',
    author_email='support@syncwerk.com',
    packages=find_packages(exclude=["Makefile.am", "pygencode.py", "test_pyrpcsyncwerk.py", "*.tests", "*.tests.*", "tests.*", "tests"]),
    url='https://www.syncwerk.com',
    license='Apache 2.0',
    description='RPC client bindings',
    long_description='Bindings for Syncwerk RPC client',
    platforms=['any'],
    include_package_data=True,
)
