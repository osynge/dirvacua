from sys import version_info
version = "0.0.2"
if version_info < (2, 6):
	from distutils.core import setup
else:
	try:
        	from setuptools import setup, find_packages
	except ImportError:
        	from ez_setup import use_setuptools
        	use_setuptools()
        	from setuptools import setup, find_packages

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
    data_files=[('/usr/share/doc/%s' % (name),['README.md','ChangeLog','LICENSE'])],
    )
