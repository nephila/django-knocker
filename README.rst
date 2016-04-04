=============================
django-knocker
=============================

.. image:: https://img.shields.io/pypi/v/django-knocker.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-knocker
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-knocker.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-knocker
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/django-knocker.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-knocker
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/django-knocker.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-knocker
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/django-knocker/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-knocker?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/django-knocker/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/django-knocker
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/django-knocker/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-knocker
   :alt: Code Climate


Channels-based desktop notification system

Documentation
-------------

The full documentation is at https://django-knocker.readthedocs.org.

Usage
-----

See https://django-knocker.readthedocs.org/en/latest/usage.rst

Features
--------

* Sends desktop notifications to connected browsers
* Multilianguage support (with `django-parler`_ and `django-hvad`_)
* Uses `django-meta`_ API for a consistent metadata handling

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python setup.py test

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage-helper`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage-helper`: https://github.com/nephila/cookiecutter-djangopackage-helper
.. _django-hvad: https://github.com/KristianOellegaard/django-hvad
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-meta: https://github.com/nephila/django-meta
