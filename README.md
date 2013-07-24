dirvacua
========

dirvacua is a directory cleaner for directories for many versioned files. Some times you want to keep the last 10.

This application attempts to only delete versions of files with more than 10 copies.


    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ dirvacua $my_development_yum_repository

Dirvacua has command line help:

    $ dirvacua --help

This will show all command line options for dirvacua.

Using dirvacua may worry users that it will delete the wrong files for this 
reason it can be told to show what files it would delete rather than delete 
files.

    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ dirvacua --nop $my_development_yum_repository

Be default dirvacua will only delete versioned files where you have more than 10
versioned copies. This can be set on the command line using the following command

    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ dirvacua --max 2 $my_development_yum_repository

This will tell dirvacua to only keep 2 copies of a versioned file in a directory.

Dirvacua using the standard logging libraries, these can be configured using the
standard python logging configuration:

    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ DIRVACUA_LOG_CONF="/etc/dirvacua/logging.conf"
    $ dirvacua $my_development_yum_repository

or alternatively overriding the environment variable:

    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ LOG_CONF="/etc/dirvacua/logging.conf"
    $ dirvacua \
      --logcfg $LOG_CONF
      $my_development_yum_repository

* How dirvacua works.

dirvacua is not powered by magic, it simply processing the file name and 
comparing with other files in the directory. Each file name is split with 
delimiters, then each file subsection is further is split into strings and 
numbers. To decide that files are the same it compares these strings, and if the
first 4 string blocks in order are the same it assumes the file is the same. If 
a number is found in the file name it is assumed this is the start of the 
visioning. The following option sets the default options:

    $ my_development_yum_repository="/pub/dev/yum/owen"
    $ dirvacua --match-string-count 4\
        --match-number-skip 0 \
        $my_development_yum_repository
