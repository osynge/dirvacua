#!/usr/bin/env python

# Copyright (c) 2012 Owen Synge
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the DESY nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Owen Synge BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import
import optparse
import os
import os.path
import re
import sys
import logging

from .__version__ import version

regdelexp = re.compile('[-,_./]')
regnumeric = re.compile('[0-9]+')


def split_line_by_delimiter(line, regex):
    splitline = []
    splititr = regex.finditer(line)
    lstart = 0
    for i in splititr:
        (mstart, mend) = i.span()
        if lstart != mstart:
            splitline.append(line[lstart:mstart])
        splitline.append(line[mstart:mend])
        lstart = mend
    linelen = len(line)
    if lstart != linelen:
        splitline.append(line[lstart:linelen])
    return splitline


def string_sort(x, y):
    xsplit = split_line_by_delimiter(x, regnumeric)
    ysplit = split_line_by_delimiter(y, regnumeric)
    ysplitlen = len(ysplit)
    xsplitlen = len(xsplit)
    minsplitlen = ysplitlen
    if xsplitlen < ysplitlen:
        minsplitlen = xsplitlen
    for i in range(minsplitlen):
        if xsplit[i] == ysplit[i]:
            continue
        if (xsplit[i].isdigit() and ysplit[i].isdigit()):
            rc = int(0)
            if int(xsplit[i]) > int(ysplit[i]):
                rc = -1
            if int(xsplit[i]) < int(ysplit[i]):
                rc = 1
            return rc
        if xsplit[i].isdigit():
            return -1
        if ysplit[i].isdigit():
            return 1
        if xsplit[i] > ysplit[i]:
            return -1
        if xsplit[i] < ysplit[i]:
            return 1
    if xsplitlen < ysplitlen:
        return 1
    if xsplitlen > ysplitlen:
        return -1
    return 0


def split_numeric_sort(x, y):
    xsplit = split_line_by_delimiter(x, regdelexp)
    ysplit = split_line_by_delimiter(y, regdelexp)
    ysplitlen = len(ysplit)
    xsplitlen = len(xsplit)
    minsplitlen = ysplitlen
    if xsplitlen < ysplitlen:
        minsplitlen = xsplitlen
    for i in range(minsplitlen):
        if xsplit[i] == ysplit[i]:
            continue
        if (xsplit[i].isdigit() and ysplit[i].isdigit()):
            rc = int(0)
            if int(xsplit[i]) > int(ysplit[i]):
                rc = -1
            if int(xsplit[i]) < int(ysplit[i]):
                rc = 1
            return rc
        if xsplit[i].isdigit():
            return -1
        if ysplit[i].isdigit():
            return 1
        rc = string_sort(xsplit[i], ysplit[i])
        if rc != 0:
            return rc
    if xsplitlen < ysplitlen:
        return 1
    if xsplitlen > ysplitlen:
        return -1
    return 0


class dirvacua:
    def __init__(self):
        self.maxitems = 10
        self.matchstringsmax = 4
        self.digitsskipmax = 0
        self.noop = True
        self.log = logging.getLogger("dirvacua")
        self.fileTypes = set([])

    def matchHash(self, filename):
        splitdelimiter = split_line_by_delimiter(filename, regdelexp)
        splitlist = []
        namestart = filename
        digitcounter = 0
        for thingy in splitdelimiter:
            tempsplit = split_line_by_delimiter(thingy, regnumeric)
            for item in tempsplit:
                if item.isdigit():
                    digitcounter += 1
                    if digitcounter < self.digitsskipmax:
                        continue
                    break
                splitlist.append(item)
                if len(splitlist) > self.matchstringsmax:
                    break
        if len(splitlist) > 2:
            namestart = ''
            for item in splitlist:
                namestart += item
        if len(namestart) == 0:
            namestart = filename
        # self.log.debug("namestart=%s" % (namestart))
        return namestart

    def OldestFiles(self, dir_path):
        log = logging.getLogger("OldestFiles")
        if not os.path.isdir(dir_path):
            log.warning("Invalid directory:%s" % (dir_path))
        files_dict = {}
        for filename in os.listdir(dir_path):
            fullpath = os.path.join(dir_path, filename)
            isMatchedType = False
            if 'file' in self.fileTypes and os.path.isfile(fullpath):
                isMatchedType = True

            if 'dir' in self.fileTypes and os.path.isdir(fullpath):
                isMatchedType = True

            if isMatchedType is False:
                continue

            namestart = self.matchHash(filename)
            if namestart not in files_dict.keys():
                files_dict[namestart] = []
            files_dict[namestart].append(filename)
        length = self.maxitems
        for key in files_dict.keys():
            workinglist = files_dict[key]
            if len(workinglist) > length:
                sortedlist = sorted(workinglist, cmp=split_numeric_sort)
                while len(sortedlist) > length:
                    item = sortedlist.pop()
                    fullpath = os.path.join(dir_path, item)
                    yield fullpath
        return

    def ExpireOldestFiles(self, dir_path):
        for filepath in self.OldestFiles(dir_path):
            if os.path.isdir(filepath):
                # With directories to full path
                for root, dirs, files in os.walk(filepath, topdown=False):
                    for name in files:
                        path = os.path.join(root, name)
                        if self.noop:
                            self.log.info("Would remove:%s" % (path))
                            continue
                        os.remove(path)
                    for name in dirs:
                        path = os.path.join(root, name)
                        if self.noop:
                            self.log.info("Would remove:%s" % (path))
                            continue
                        os.rmdir(path)
                if self.noop:
                    self.log.info("Would remove:%s" % (filepath))
                    continue
                os.rmdir(filepath)
            else:
                if self.noop:
                    self.log.info("Would remove:%s" % (filepath))
                    continue
                self.log.debug("Removing:%s" % (filepath))
                os.remove(filepath)

    def ExpireOldestFilesRecurse(self, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for d in dirs:
                fullpath = os.path.join(root, d)
                self.ExpireOldestFiles(fullpath)
        self.ExpireOldestFiles(dir_path)


def main():
    """Runs program and handles command line options"""
    p = optparse.OptionParser(version="%prog " + version)
    p.add_option('-L', '--logcfg', action='store', help='Logfile configuration file.', metavar='DIRVACUA_LOG_CONF')
    p.add_option('-v', '--verbose', action='count', help='Change global log level, increasing log output.', metavar='LOGFILE')
    p.add_option('-q', '--quiet', action='count', help='Change global log level, decreasing log output.', metavar='LOGFILE')
    p.add_option('--noop', action='store_true', help='Show files that woudl be removed.', metavar='LOGFILE')
    p.add_option('--max', action='store', help='Set the maximum number of file versions allowed.', metavar='MAXFILES')
    p.add_option('--recurse', action='store_true', help='Recursively work on directories.', metavar='LOGFILE')
    p.add_option('--match-string-count', action='store', help='Set the maximum number string sections to match.')
    p.add_option('--match-number-skip', action='store', help='Set the maximum number string sections to match.')
    p.add_option('--files', action='store_true', help='Work on files. (default)')
    p.add_option('--dirs', action='store_true', help='Work on directories.')
    options, arguments = p.parse_args()
    # Set up basic variables
    logFile = None
    nodelete = False
    maxversions = 10
    recurse = False
    matchstringsmax = 4
    matchnumberskip = 0
    matchFileType = set([])
    # Read enviroment variables
    if 'DIRVACUA_LOG_CONF' in os.environ:
        logFile = os.environ['DIRVACUA_LOG_CONF']
    # Set up log file
    LoggingLevel = logging.WARNING
    LoggingLevelCounter = 2
    if options.verbose:
        LoggingLevelCounter = LoggingLevelCounter - options.verbose
        if options.verbose == 1:
            LoggingLevel = logging.INFO
        if options.verbose == 2:
            LoggingLevel = logging.DEBUG
    if options.quiet:
        LoggingLevelCounter = LoggingLevelCounter + options.quiet
    if LoggingLevelCounter <= 0:
        LoggingLevel = logging.DEBUG
    if LoggingLevelCounter == 1:
        LoggingLevel = logging.INFO
    if LoggingLevelCounter == 2:
        LoggingLevel = logging.WARNING
    if LoggingLevelCounter == 3:
        LoggingLevel = logging.ERROR
    if LoggingLevelCounter == 4:
        LoggingLevel = logging.FATAL
    if LoggingLevelCounter >= 5:
        LoggingLevel = logging.CRITICAL

    if options.logcfg:
        logFile = options.logcfg
    if options.noop:
        nodelete = True
    if options.recurse:
        recurse = True
    if options.max:

        maxversions = int(options.max)

    if logFile is not None:
        if os.path.isfile(str(options.log_config)):
            logging.config.fileConfig(options.log_config)
        else:
            logging.basicConfig(level=LoggingLevel)
            log = logging.getLogger("main")
            log.error("Logfile configuration file '%s' was not found." % (options.log_config))
            sys.exit(1)
    else:

        logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    # Now process command line
    targets = []
    if options.max:
        maxversions = int(options.max)
    if options.match_string_count:
        matchstringsmax = int(options.match_string_count)
    if options.match_number_skip:
        matchnumberskip = int(options.match_number_skip)
    if options.files:
        matchFileType.add('file')
    if options.dirs:
        matchFileType.add('dir')
    if len(matchFileType) == 0:
        matchFileType.add('file')
        log.info("Matching files by default.")
    # options, arguments
    for arg in arguments:
        targets.append(arg)
    if len(targets) == 0:
        log.info("list directories to vacuum at the end of the command line.")
        log.error("no directories specified to vacuum.")
        sys.exit(2)
    if matchstringsmax < 1:
        log.error("Number of strings to match must be 1 or greater.")
        sys.exit(3)
    processor = dirvacua()
    processor.noop = nodelete
    processor.maxitems = maxversions
    processor.matchstringsmax = matchstringsmax
    processor.digitsskipmax = matchnumberskip
    processor.fileTypes = matchFileType
    for thisdir in arguments:
        if not os.path.isdir(thisdir):
            log.error("Could not find directory path:%s" % (thisdir))
            continue
        if recurse is True:
            processor.ExpireOldestFilesRecurse(thisdir)
        else:
            processor.ExpireOldestFiles(thisdir)


if __name__ == "__main__":
    main()
