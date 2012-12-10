req
===

``req`` discovers your Python requirements.

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

``req`` to the rescue!

Usage
-----

In your ``setup.py``::

    from setuptools import setup, find_packages

    from req import find_requirements

    setup(
        name='my-package',
        packages=find_packages(),

        # Find requirements the same as you finds packages
        setup_requires=['req'],
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
    >>> from req import get_requirement_filenames
    >>> get_requirement_filenames('deps')
    # TODO(dejw): output

Note that ``find_packages`` will not look for requirements recursively, it
assumes instead that all files are in the same directory.

Dependency groups
~~~~~~~~~~~~~~~~~

You can specify a dependency group (or groups) by adding ``group`` arguments
respectively::

    >>> get_requirement_filenames(group='devel')
    # TODO(dejw): output
    >>> get_requirement_filenames(group=['devel', 'ci'])
    # TODO(dejw): output

In order not to use base requirements you can use ``only`` attribute, which can
be handy in following case::

    >>> get_requirement_filenames(only='setup') # also accepts a list
    # TODO(dejw): output

Prerequisites
-------------

``req`` requires only ``pip`` to work (which you probably already have
installed), besides standard library.