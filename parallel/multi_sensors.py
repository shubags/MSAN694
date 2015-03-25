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

"""
Demonstrates the use of multi-processing for infinite streams of data.

Many producers (``Sensor`` objects) will generate an infinite stream of data that will be
queued for a single consumer to analyze and take action on.
"""

from __future__ import print_function


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


def log(msg):
    with console_lock:
        print(msg)


def producer(queue, delay=0.500):
    """ It will forever put the sensor's readings onto the queue

    :param queue: the queue to push sensor data to
    :param delay: between readings
    :return: None
    """
    with pid_file_lock:
        with open(pid_file, mode='a') as pid:
            pid.write('{}\n'.format(os.getpid()))
    log("[{}] producer started".format(os.getpid()))
    sensor = Sensor(faulty_pct=30.0)
    try:
        for value in sensor.get():
            queue.put(value)
            time.sleep(delay)
    except KeyboardInterrupt:
        # User pressed Ctrl-C, safe to ignore
        pass


def consumer(queue, idx, threshold=5, shared=None):
    """ Reads values from the queue and raises an alarm

    More than ```threshold``` consecutive values that are True will trigger an alarm.

    :param queue: the queue to read from
    :param threshold: The threshold at which we trigger the alarm, across ALL monitors
    :param shared: an optional shared ```Value`` for multiple Monitors
    :type shared: multiprocessing.Value
    :return: never, unless the threshold is exceeded
    """
    log("[monitor: {}] Started with threshold {}".format(os.getpid(), threshold))
    count = 0
    try:
        while shared.value < threshold:
            reading = queue.get(block=True)
            if reading:
                count += 1
                log('Alerting: {}'.format(count))
            else:
                # reset the counter
                count = 0
            if shared is not None:
                with shared.get_lock():
                    # NOTE: the double-check, as things may have changed between the test on the
                    # while and here; not doing this, causes some monitors to never terminate
                    if count == 0 and shared.value < threshold:
                        shared.value = 0
                    else:
                        shared.value += count
        log("[monitor-{}] Threshold exceeded - exiting".format(idx))
    except KeyboardInterrupt:
        # User pressed Ctrl-C, safe to ignore
        pass


def main(conf):
    # FIXME: poor man's MP pool - use multiprocessing.Pool in real production code
    sensors_pool = []
    monitors_pool = []
    queue = mp.Queue()

    # Shared memory, to share state between processes - this is best left to the experts!
    shared_value = mp.Value('i', 0)
    for k in range(conf.monitors):
        monitor = mp.Process(target=consumer, name="Monitor",
                             args=(queue, k, conf.threshold, shared_value))
        monitors_pool.append(monitor)
        monitor.start()
    for i in range(conf.sensors):
        proc_name = 'Proc-{}'.format(i)
        process = mp.Process(target=producer, name=proc_name, args=(queue,))
        process.start()
        sensors_pool.append(process)
    log("[main: {}] waiting for {} monitors to complete (when threshold is exceeded)"
        .format(os.getpid(), conf.monitors))
    try:
        for monitor in monitors_pool:
            monitor.join()
    except KeyboardInterrupt:
        # User pressed Ctrl-C, safe to ignore
        pass
    for process in sensors_pool:
        process.terminate()
    with pid_file_lock:
        os.remove(pid_file)
    log("[main: {}] finished".format(os.getpid()))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensors', type=int, default=10,
                        help="Number of sensors to activate")
    parser.add_argument('--threshold', required=False, default=2, type=int,
                        help="Alarm threshold")
    parser.add_argument('--monitors', type=int, default=1,
                        help="Number of monitoring processes")
    return parser.parse_args()


if __name__ == "__main__":
    config = parse_args()
    main(config)
