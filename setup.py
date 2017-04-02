from sys import version_info
from pydirvacua.__version__ import version
if version_info < (2, 6):
	from distutils.core import setup
else:
	try:
        	from setuptools import setup, find_packages
	except ImportError:
        	from ez_setup import use_setuptools
        	use_setuptools()
        	from setuptools import setup, find_packages



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


name='dirvacua'
setup(name=name,
    version=version,
    description="""dirvacua is a directory vacuuming tool.""",
    long_description="""Should you want to keep only the last "N" files of each type from a directory that contains files from multiple source deleteing based up on time may not be enough. dirvacua aims to clearly see which fiels are versions and only delete the older versioned files.""",
    author="O M Synge",
    author_email="",
    license='Apache License (2.0)',
    url = 'git://github.com/osynge/dirvacua.git',
    classifiers=[
        'Development Status :: 4 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    scripts=['dirvacua'],
    packages = ['pydirvacua', 'pydirvacua.tests'],
    data_files=[
        ('/usr/share/doc/%s' % (name),['README.md','ChangeLog','LICENSE'])
    ]
    ,
    tests_require=[
        'coverage >= 3.0',
        'pytest',
        'mock',
    ],
    setup_requires=[
        'nose',
    ],
    cmdclass = {'test': PyTest},
    )

