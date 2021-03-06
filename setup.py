from setuptools import setup

setup(
    name='simpleconsent',
    version='0.1.0',
    description='Consent service for SATOSA',
    author='r2h2',
    author_email='rh@identinetics.com',
    license='MIT',
    url='https://github.com/identinetics/simpleconsent',
    packages=['simpleconsent', ],
    install_requires=[
        "django >=2.2.10, <3.0",  # avoid 3.0 alpha release
        "django-basicauth",
        "jinja2",  # why not django templates? Make it easy to load template from random filesystem path
        "requests",
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
