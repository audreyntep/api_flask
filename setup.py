from setuptools import setup, find_packages
setup(
    name='g3api',
    version='0.1.0',
    long_description=__doc__,
    packages=['yourapplication'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
