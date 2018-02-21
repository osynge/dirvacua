from sys import version_info
import os
import os.path
from pydirvacua.__version__ import version

if version_info < (2, 6):
    import sys
    print "Please use a newer version of python"
    sys.exit(1)

if version_info > (2, 7):
    try:
        from setuptools import setup, find_packages
    except ImportError:
	    try:
                from distutils.core import setup
	    except ImportError:
                from ez_setup import use_setuptools
                use_setuptools()
                from setuptools import setup, find_packages



def determine_path ():
    """Borrowed from wxglade.py"""
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print ("I'm sorry, but something is wrong.")
        print ("There is no __file__ variable. Please contact the author.")
        sys.exit ()

from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

needs_scripts = True
needs_jobs = True
needs_docs = True

if "VIRTUAL_ENV" in os.environ:
    needs_scripts = False
    needs_jobs = False
    needs_docs = False

if "WITHOUT_DOC" in os.environ:
    needs_docs = False


name = "dirvacua"
setup_args = {
    "name" : name,
    "version" : version,
    "description" : """dirvacua is a directory vacuuming tool.""",
    "long_description" : """Should you want to keep only the last "N" files of each type from a directory that contains files from multiple source deleteing based up on time may not be enough. dirvacua aims to clearly see which fiels are versions and only delete the older versioned files.""",
    "author" : "O M Synge",
    "author_email" : "",
    "license" : 'Apache License (2.0)',
    "url" : 'git://github.com/osynge/dirvacua.git',
    "classifiers" : [
        'Development Status :: 4 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    "scripts" : ['dirvacua'],
    "packages" : ['pydirvacua', 'pydirvacua.tests'],
    "tests_require" : [
        'coverage >= 3.0',
        'pytest',
        'mock',
    ],
    "setup_requires" : [],
    "cmdclass" : {'test': PyTest},
    }

if needs_jobs or needs_scripts or needs_docs:
    data_files = []
    path = determine_path ()
    if needs_docs is True:
        installdir_doc = "/usr/share/doc/%s-%s" % (name,version)
        data_files.append((installdir_doc,['README.md','LICENSE','ChangeLog']))
    setup_args["data_files"] = data_files

setup(**setup_args)
