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

from __future__ import print_function


__author__ = 'marco'


import multiprocessing as mp
import time


shared_file = '/tmp/multi_file.txt'


def p1(lock):
    with lock:
        with open(shared_file, 'w') as shf:
            shf.write("this is written by P1\n")
    print("P1 done")


def p2(lock):
    with lock:
        with open(shared_file, 'r') as shf:
            line = shf.readline()
    print("[P2] line: " + line)
    print("P2 done")


def main():
    shared_file_lock = mp.Lock()
    proc1 = mp.Process(target=p1, name="proc-1", args=(shared_file_lock,))
    proc2 = mp.Process(target=p2, name="proc-2", args=(shared_file_lock,))
    print("main: starting processes")
    proc1.start()
    time.sleep(0.5)
    proc2.start()
    print("main: done starting")
    proc2.join()
    proc1.join()


if __name__ == '__main__':
    main()
