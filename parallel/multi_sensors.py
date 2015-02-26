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

import multiprocessing as mp
import thread

# example with shared memory - avoid

# example with queue - each process sleeps 1 sec, main proc polls q to check if majority report
# leak assume controller much faster

# then use with 'infinite loop' and trigger leak: use a 'sleeper' thread that triggers leak,
# pass in the Sensors and randomly trigger a bunch of them


def main():
    pass


if __name__ == "__main__":
    main()
