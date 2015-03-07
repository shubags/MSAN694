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

import boto
from boto import ec2


def main():
    """ Connects to AWS using the default configuration file (```~/.aws/credentials```)

    :return:
    """
    conn = boto.connect_ec2()
    print(conn.get_all_instances())

    print(ec2.connect_to_region('us-west-1'))

if __name__ == "__main__":
    main()
