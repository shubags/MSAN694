#!/usr/bin/env python
#
# Copyright AlertAvert.com (c) 2013. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'marco'


import os
import re
import requests

BOOKMARKS_DATA_FILE = 'data/bookmarks.html'


def get_cwd():
    """ Find the current, absolute path that this script is being executed from

    :return: the absolute path of the currently executing python script
    """
    return os.path.abspath(os.path.dirname(__file__))


def main():
    fname = os.path.join(get_cwd(), BOOKMARKS_DATA_FILE)
    with open(fname) as bk:
        lines = [line.strip() for line in bk]
        one_line = ''.join(lines)

    # FIXME: this is the most naive RegEx for a URLs I can think of
    m = re.findall(r'http://[\w.]*', one_line, re.IGNORECASE)
    # TODO: cleaning: m.sort()
    print("Found {} URLs".format(len(m)))

    print("Requesting {}".format(m[100]))
    page = requests.get(m[100])
    print(page.content)


if __name__ == "__main__":
    main()
