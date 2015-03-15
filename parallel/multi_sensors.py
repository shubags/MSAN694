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


import argparse
import multiprocessing as mp
import os
import time

from sensors import Sensor

# FIXME: Globals are evil, avoid in real production code
pid_file = '/tmp/multi_sensors.pid'
pid_file_lock = mp.Lock()
console_lock = mp.Lock()


def log(s):
    with console_lock:
        print(s)


def producer(q, delay=0.500):
    """ It will forever put the sensor's readings onto the queue

    :param q: the queue to push sensor data to
    :param delay: between readings
    :return: None
    """
    with pid_file_lock:
        with open(pid_file, mode='a') as pid:
            pid.write('{}\n'.format(os.getpid()))
    log("[{}] producer started".format(os.getpid()))
    sensor = Sensor(faulty_pct=30.0)
    for x in sensor.get():
        q.put(x)
        time.sleep(delay)


def consumer(q, threshold=5):
    """ Reads values from the queue and raises an alarm if more than ```threshold``` consecutive values are True

    :param q: the queue to read from
    :return: never, unless the threshold is exceeded
    """
    log("[monitor: {}] Started with threshold {}".format(os.getpid(), threshold))
    count = 0
    while count < threshold:
        reading = q.get(block=True)
        if reading:
            count += 1
            log('Alerting: {}'.format(count))
        else:
            # reset the counter
            count = 0
    log("[monitor] Threshold exceeded - exiting")


def main(conf):
    # TODO: poor man's MP pool - use multiprocessing.Pool in real production code
    pool = []
    q = mp.Queue()
    monitor = mp.Process(target=consumer, name="Monitor", args=(q, conf.threshold))
    monitor.start()
    for i in range(conf.sensors):
        proc_name = 'Proc-{}'.format(i)
        p = mp.Process(target=producer, name=proc_name, args=(q,))
        p.start()
        pool.append(p)
    log("[main: {}] waiting for monitor to complete (when threshold is exceeded)".format(os.getpid()))
    monitor.join()
    for p in pool:
        p.terminate()
    with pid_file_lock:
        os.remove(pid_file)
    log("[main: {}] finished".format(os.getpid()))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensors', type=int, default=10,
                        help="Number of sensors to activate")
    parser.add_argument('--threshold', required=False, default=2, type=int,
                        help="Alarm threshold")
    return parser.parse_args()


if __name__ == "__main__":
    conf = parse_args()
    main(conf)
