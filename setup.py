# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REST API for invenio-records."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'Flask-Login>=0.3.2',
    'invenio-db[all]>=1.0.2',
    'invenio-indexer>=1.0.0',
    'invenio-config>=1.0.2',
    'pytest-invenio>=1.2.1',
    'jsonref==1.0.1',
    'mock>=4'
]

invenio_search_version = '1.2.3,<1.3.0'

extras_require = {
    'elasticsearch7': [
        'invenio-search[elasticsearch7]>=2.1.0,<3.0.0'
    ],
    'opensearch1': [
        'invenio-search[opensearch1]>=2.1.0,<3.0.0'
    ],
    'opensearch2': [
        'invenio-search[opensearch2]>=2.1.0,<3.0.0'
    ],
    'citeproc': [
        'citeproc-py==0.3.0',
        'citeproc-py-styles==0.1.0',
    ],
    'datacite': [
        'datacite==1.0.1',
        'urllib3>=1.21.1,<1.27'
    ],
    'docs': [
        'Sphinx>=3'
    ],
    'dublincore': [
        'dcxml>=0.1.0',
    ],
    'jsonld': [
        'pyld>=0.7.1,<2',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in (
        'elasticsearch7',
        'opensearch1',
        'opensearch2'
    ):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'bleach>=2.1.3',
    'ftfy>=4.4.3',
    'invenio-base',
    'invenio-pidstore>=1.2.1,<2.0.0',
    'invenio-records>=2.0.0,<3.0.0',
    'invenio-rest>=1.2.4,<2.0.0',
    'invenio-indexer>=2.1.0,<3.0.0',
    'invenio-i18n>=2.0.0,<3.0.0',
    'importlib-metadata>=4.0.0,<5.0.0',
    'SQLAlchemy==1.4',
    'sqlalchemy-utils==0.38.3',
    "SQLAlchemy-Continuum @ git+https://github.com/inspirehep/sqlalchemy-continuum.git"
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_records_rest', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-records-rest',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio api',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-records-rest',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.api_apps': [
            'invenio_records_rest = invenio_records_rest:InvenioRecordsREST',
        ],
        'invenio_base.converters': [
            'pid = invenio_records_rest.utils:PIDConverter',
            'pidpath = invenio_records_rest.utils:PIDPathConverter',
        ],
        'invenio_base.api_blueprints': [
            ('invenio_records_rest = '
             'invenio_records_rest.views:create_blueprint_from_app'),
        ],
        'invenio_base.api_converters': [
            'pid = invenio_records_rest.utils:PIDConverter',
            'pidpath = invenio_records_rest.utils:PIDPathConverter',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_records_rest',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
    ],
)
