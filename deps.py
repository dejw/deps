# -*- coding: utf-8 -*-

"""deps discovers your Python requirements."""

import itertools
import os
import sys

from pip import req

__version__ = '0.1.0'


def get_requirement_filenames(where=None, group=None, only=None, version=None,
                              extension='txt'):
    """Produces requirements filenames based on group and interpreter version.

    Filenames are following pattern:

        [group-]?requirements[-version+]?.txt

    For instance, for prefix `devel` and `version` (2, 7, 3) it will produce:

              requirements.txt
              requirements-2.txt
              requirements-27.txt
              requirements-273.txt
        devel-requirements.txt
        devel-requirements-2.txt
        devel-requirements-27.txt
        devel-requirements-273.txt

    Args:
        where: str, a base for filenames
        group: str or list, a prefix for requirements, like 'dev', 'devel',
            ['devel', 'prod']
        only: str or list, the same as group, but setting this will ommit base
            requirements
        version: an iterable, with version segments to use, using
            os.version_info by default
        extension: str, what extension to use, 'txt' by default

    Returns:
        a list of filenames
    """

    if group is not None and only is not None:
        raise ValueError('group and only arguments are mutually exclusive')

    groups = ['']

    if only is not None:
        group = only
        groups = []

    if group is not None:
        if not isinstance(group, list):
            group = [group]

        groups.extend('%s-' % g for g in group if g)

    groups = [str(g) for g in groups]

    version = sys.version_info if version is None else version
    version = map(str, version)
    version = [v for v in version if v and v != '.']
    version = [''] + ['-%s' % ''.join(version[:i + 1])
                      for i, v in enumerate(version)]

    names = []
    for g, v in itertools.product(groups, version):
        filename = '%srequirements%s.%s' % (g, v, extension)

        if where:
            filename = os.path.join(where, filename)

        names.append(filename)

    return names


def find_requirements(where=None, group=None, only=None, version=None):
    """Generates requirements based on given prefix and version.

    It works similar to find_packages function. It accepts where argument
    and yields install requiremnets.

    Note that this function will not search for requirement files recursively -
    it expects that all files are in the same directory.

    Args:
        where: a directory where requirement files resides
        group: a configuration prefix, like 'devel', ['prod', 'stage']
        only: the same as group, but will ommit base requiremnets
        version: what version of python to use, current by default

    Returns:
        a list of requiremnets
    """

    class FakeOptions(object):
        skip_requirements_regex = None
        default_vcs = ''

    reqs = []

    for filename in get_requirement_filenames(where=where, group=group,
                                              only=only, version=version):
        if os.path.exists(filename):
            for install_req in req.parse_requirements(filename,
                                                      options=FakeOptions()):
                reqs.append(str(install_req.req))

    return reqs
