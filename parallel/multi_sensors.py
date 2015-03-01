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
from sensors import Sensor

__author__ = 'marco'

import multiprocessing as mp
import os
import time


def producer(q, delay=0.500):
    """ It will forever put the sensor's readings onto the queue

    :param q: the queue to push sensor data to
    :param delay: between readings
    :return: None
    """
    print("[{}] producer started".format(os.getpid()))
    sensor = Sensor(faulty_pct=30.0)
    for x in sensor.get():
        q.put(x)
        time.sleep(delay)


def consumer(q, threshold=5):
    """ Reads values from the queue and raises an alarm if more than ```threshold``` consecutive values are True

    :param q: the queue to read from
    :return: never, unless the threshold is exceeded
    """
    print("[monitor] Started with threshold {}".format(threshold))
    count = 0
    while count < threshold:
        reading = q.get(block=True)
        if reading:
            count += 1
        else:
            # reset the counter
            count = 0
    print("[monitor] Threshold exceeded - exiting")


def main():
    pool = []
    q = mp.Queue()
    monitor = mp.Process(target=consumer, name="Monitor", args=(q, 2))
    monitor.start()
    for i in range(10):
        proc_name = 'Proc-{}'.format(i)
        p = mp.Process(target=producer, name=proc_name, args=(q,))
        p.start()
        pool.append(p)
    print("[main: {}] waiting for monitor to complete (when threshold is exceeded)".format(os.getpid()))
    monitor.join()
    for p in pool:
        p.terminate()
    print("[main: {}] finished".format(os.getpid()))


if __name__ == "__main__":
    main()
