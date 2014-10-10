"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from setuptools import setup


setup(
    name='django-registration',
    description = 'An extensible application for registering users.',
    version='0.0.1',
    author='Jaime Pajuelo',
    author_email='jaimepk27@gmail.com',
    license='BSD 2-Clause',
    url='https://github.com/jpajuelo/django-registration',
    packages=['registration'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities'
    ]
)
