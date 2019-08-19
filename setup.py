from setuptools import setup

setup(
    name='simpleconsent',
    version='0.0.1',
    description='Consent srevice for SATOSA',
    author='r2h2',
    author_email='rh@identinetics.com',
    license='MIT',
    url='https://github.com/identinetics/simpleconsent',
    packages=['simpleconsent', ],
    package_dir={'': 'src'},
    install_requires=[
        "django",
        "djangorestframework",
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
