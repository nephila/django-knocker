=============================
django-knocker
=============================

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

Channels-based desktop notification system

***************
Documentation
***************

The full documentation is at https://django-knocker.readthedocs.io.

***************
Usage
***************

See https://django-knocker.readthedocs.io/en/latest/usage.html


***************
Features
***************

* Sends desktop notifications to connected browsers
* Multilianguage support (with `django-parler`_ and `django-hvad`_)
* Uses `django-meta`_ API for a consistent metadata handling

***************
Running Tests
***************

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python cms_helper.py

***************
Credits
***************

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage-helper`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage-helper`: https://github.com/nephila/cookiecutter-djangopackage-helper
.. _django-hvad: https://github.com/KristianOellegaard/django-hvad
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-meta: https://github.com/nephila/django-meta



.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Python versions

.. |Status| image:: https://img.shields.io/travis/nephila/django-meta.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-meta
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/django-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-meta?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/django-meta.svg?style=flat-square
   :target: https://pypi.python.org/pypi/django-meta/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/django-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-meta
   :alt: Code Climate
