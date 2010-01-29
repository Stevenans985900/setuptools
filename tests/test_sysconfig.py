"""Tests for distutils.sysconfig."""
import os
import test
import unittest

from distutils import sysconfig
from distutils.tests import support
from test.support import TESTFN, run_unittest

class SysconfigTestCase(support.EnvironGuard,
                        unittest.TestCase):
    def setUp(self):
        super(SysconfigTestCase, self).setUp()
        self.makefile = None

    def tearDown(self):
        if self.makefile is not None:
            os.unlink(self.makefile)
        self.cleanup_testfn()
        super(SysconfigTestCase, self).tearDown()

    def cleanup_testfn(self):
        if os.path.isfile(TESTFN):
            os.remove(TESTFN)
        elif os.path.isdir(TESTFN):
            shutil.rmtree(TESTFN)

    @support.capture_warnings
    def test_get_python_lib(self):
        lib_dir = sysconfig.get_python_lib()
        # XXX doesn't work on Linux when Python was never installed before
        #self.assertTrue(os.path.isdir(lib_dir), lib_dir)
        # test for pythonxx.lib?
        self.assertNotEqual(sysconfig.get_python_lib(),
                            sysconfig.get_python_lib(prefix=TESTFN))
        _sysconfig = __import__('sysconfig')
        res = sysconfig.get_python_lib(True, True)
        self.assertEquals(_sysconfig.get_path('platstdlib'), res)

    @support.capture_warnings
    def test_get_python_inc(self):
        inc_dir = sysconfig.get_python_inc()
        # This is not much of a test.  We make sure Python.h exists
        # in the directory returned by get_python_inc() but we don't know
        # it is the correct file.
        self.assertTrue(os.path.isdir(inc_dir), inc_dir)
        python_h = os.path.join(inc_dir, "Python.h")
        self.assertTrue(os.path.isfile(python_h), python_h)

    @support.capture_warnings
    def test_parse_makefile_base(self):
        self.makefile = TESTFN
        fd = open(self.makefile, 'w')
        fd.write(r"CONFIG_ARGS=  '--arg1=optarg1' 'ENV=LIB'" '\n')
        fd.write('VAR=$OTHER\nOTHER=foo')
        fd.close()
        d = sysconfig.parse_makefile(self.makefile)
        self.assertEquals(d, {'CONFIG_ARGS': "'--arg1=optarg1' 'ENV=LIB'",
                              'OTHER': 'foo'})

    def test_parse_makefile_literal_dollar(self):
        self.makefile = TESTFN
        fd = open(self.makefile, 'w')
        fd.write(r"CONFIG_ARGS=  '--arg1=optarg1' 'ENV=\$$LIB'" '\n')
        fd.write('VAR=$OTHER\nOTHER=foo')
        fd.close()
        d = sysconfig.parse_makefile(self.makefile)
        self.assertEquals(d, {'CONFIG_ARGS': r"'--arg1=optarg1' 'ENV=\$LIB'",
                              'OTHER': 'foo'})


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SysconfigTestCase))
    return suite


if __name__ == '__main__':
    run_unittest(test_suite())
