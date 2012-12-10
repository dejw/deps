# -*- coding: utf-8 -*-

import os
import sys

import its
try:
    from mox3 import mox
except ImportError:
    if its.py3:
        raise
    import mox

try:
    import unittest2 as unittest
except ImportError:
    if its.py2 and not its.py27:
        raise
    import unittest

from pip import req as pip_req

import req


class TestBase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.ResetAll()


class TestGetRequirementsFilenames(unittest.TestCase):

    def test_empty(self):
        names = list(req.get_requirements_filenames(group='', version=''))

        self.assertEqual(['requirements.txt'], names)

    def test_prefix_and_version(self):
        names = list(req.get_requirements_filenames(group='devel',
                     version=(2, 7, 3)))

        self.assertEqual([
            'requirements.txt',
            'requirements-2.txt',
            'requirements-27.txt',
            'requirements-273.txt',
            'devel-requirements.txt',
            'devel-requirements-2.txt',
            'devel-requirements-27.txt',
            'devel-requirements-273.txt',
        ], names)

        self.assertIsInstance(names, list)

    def test_no_prefix(self):
        names = list(req.get_requirements_filenames(version=(2, 7, 3)))

        self.assertEqual([
            'requirements.txt',
            'requirements-2.txt',
            'requirements-27.txt',
            'requirements-273.txt',
        ], names)

    def test_version_info(self):
        names = list(req.get_requirements_filenames(group='prod',
                     version=sys.version_info))

        self.assertIn('requirements.txt', names)
        self.assertIn('requirements-%s.txt' % sys.version_info.major, names)

        self.assertIn('prod-requirements.txt', names)
        self.assertIn('prod-requirements-%s.txt' % sys.version_info.major,
                      names)

    def test_version_as_str(self):
        names = list(req.get_requirements_filenames(version="2.1"))

        self.assertEqual([
            'requirements.txt',
            'requirements-2.txt',
            'requirements-21.txt',
        ], names)

    def test_source_dir(self):
        names = list(req.get_requirements_filenames(where="/tmp",
                     version="2"))

        self.assertEqual([
            '/tmp/requirements.txt',
            '/tmp/requirements-2.txt',
        ], names)

    def test_group_with_list(self):
        names = req.get_requirements_filenames(group=['a', 'b'], version='')

        self.assertEqual([
            'requirements.txt',
            'a-requirements.txt',
            'b-requirements.txt',
        ], names)

    def test_only(self):
        names = req.get_requirements_filenames(only='setup', version='')

        self.assertEqual([
            'setup-requirements.txt',
        ], names)

    def test_only_with_list(self):
        names = req.get_requirements_filenames(only=['a', 'b'], version='')

        self.assertEqual([
            'a-requirements.txt',
            'b-requirements.txt',
        ], names)

    def test_only_and_group_ValueError(self):
        with self.assertRaises(ValueError):
            req.get_requirements_filenames(only='a', group='b')


class TestFindRequirements(TestBase):

    def test_simple(self):
        prefix = 'prefix'
        version = 'version'
        source_dir = 'source dir'
        names = ['requirements.txt']
        requirements = [
            pip_req.InstallRequirement.from_line('some-package>1'),
            pip_req.InstallRequirement.from_line('other-package'),
        ]

        self.mox.StubOutWithMock(req, 'get_requirements_filenames')
        req.get_requirements_filenames(
            where=source_dir, only=None, group=prefix,
            version=version).AndReturn(names)

        self.mox.StubOutWithMock(pip_req, 'parse_requirements')
        pip_req.parse_requirements(
            'requirements.txt',
            options=mox.IgnoreArg()).AndReturn(requirements)

        self.mox.StubOutWithMock(os.path, 'exists')
        os.path.exists('requirements.txt').AndReturn(True)

        self.mox.ReplayAll()

        reqs = req.find_requirements(source_dir, group=prefix, version=version)

        self.mox.VerifyAll()
        self.assertEqual(['some-package>1', 'other-package'], reqs)


if __name__ == '__main__':
    unittest.main()
