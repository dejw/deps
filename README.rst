deps
====

.. image:: https://secure.travis-ci.org/dejw/deps.png

(`Travis <http://travis-ci.org/dejw/vip>`_)


``deps`` discovers your Python requirements.

Motivation
----------

You probably have a ``requirements.txt`` file that lists all development
dependencies (if you do not, you should have).

You can use this file in your ``setup.py`` and put its contents to
``install_requires`` argument, but sometimes, your project depends on different
packages depending on the Python version.

In this case you probably would rather build requirement list dynamically in
``setup.py`` file. This leads to two dependency lists, which are very hard to
keep synced.

``deps`` for the rescue!

Usage
-----

In your ``setup.py``::

    from setuptools import setup, find_packages

    try:
        from deps import find_requirements
    except ImportError:
        # Download latest deps.py module, in order to be able to resolve
        # dependencies *before* running any setup.py command.
        import urllib
        urllib.urlretrieve('https://raw.github.com/dejw/deps/master/deps.py', 'deps.py')
        from deps import find_requirements

    setup(
        name='my-package',
        packages=find_packages(),

        # Find requirements the same as you finds packages
        install_requires=find_requirements(),

        # ...
    )

In your ``MANIFEST.in`` file add (if you do not have one, create it)::

   include *requirements*.txt

This will include all your requirement files inside the distribution, so
``setup.py`` will be able to use them during the installation.

Requirement files
~~~~~~~~~~~~~~~~~

You can list all *base* dependencies in ``requirements.txt``. Also,
``find_requirements`` will include additional requirement files based on
current Python interpreter version, e.g:  for Python::

    >>> import sys
    >>> sys.version_info
    sys.version_info(major=2, minor=7, micro=3, releaselevel='final', serial=0)
    >>> tuple(sys.version_info)
    (2, 7, 3, 'final', 0)

following files will be used::

   requirements.txt
   requirements-2.txt
   requirements-27.txt
   requirements-273.txt
   requirements-237final.txt
   requirements-237final0.txt

With this in mind it is very easy to manage separate dependencies for Python
3.x and 2.x.

You can specify where your requirement files are::

    # get_requirement_filenames is used by find_packages internally
    >>> from deps import get_requirement_filenames
    >>> get_requirement_filenames('deps')
    ['deps/requirements.txt',
     'deps/requirements-2.txt',
     'deps/requirements-27.txt',
     'deps/requirements-273.txt',
     'deps/requirements-273final.txt',
     'deps/requirements-273final0.txt']

Note that ``find_packages`` will not look for requirements recursively, it
assumes instead that all files are in the same directory.

Dependency groups
~~~~~~~~~~~~~~~~~

You can specify a dependency group (or groups) by adding ``group`` arguments
respectively::

    >>> get_requirement_filenames(group='devel')
    ['requirements.txt',
     'requirements-2.txt',
     ... snip
     'devel-requirements.txt',
     'devel-requirements-2.txt',
     ... snip]
    >>> get_requirement_filenames(group=['devel', 'ci'])
    ['requirements.txt',
      ... snip
     'devel-requirements.txt',
      ... snip
     'ci-requirements.txt'
     ... snip]

In order not to use base requirements you can use ``only`` attribute, which can
be handy in following case::

    >>> get_requirement_filenames(only='setup') # also accepts a list
    ['setup-requirements.txt', ...]

Prerequisites
-------------

``deps`` requires only ``pip`` to work (which you probably already have
installed), besides standard library.