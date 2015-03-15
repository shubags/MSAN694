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

from __future__ import print_function

__author__ = 'marco'

import argparse
import logging
import random
import time


class Sensor(object):

    def __init__(self, faulty_pct=1.0):
        """A sensor that detects whether a leak occurred.

        This is cheap stuff: ```faulty_pct```% of the time it will give the wrong output.

        :param faulty_pct: the % of times the sensor emits the wrong reading, must be between 0
                           and 100 (exclusive)
        :type faulty_pct: float
        """
        self._alarm = False
        if not (0 < faulty_pct < 100):
            faulty_pct = 1.0
        self._range = int(100.0 / faulty_pct)
        logging.debug("Created sensor with an expected failure rate of {}%".format(faulty_pct))

    def _detect_leak(self):
        """ A radioactive leak will trigger this method """
        self._alarm = True

    def _reset(self):
        """ And we can manually reset the sensor, in case want to avoid bad press """
        self._alarm = False

    def get(self):
        """ Generator method for the sensor, returns an infinite stream of sensor readings

        :return: this is a generator method, yields the random value
        :rtype: iterator
        """
        while True:
            # A fair amount of the time this sensor will misreport its readings - because top
            # management wanted to save money and, obviously, the radioactivity detectors seemed
            # the most reasonable place where to go cheapo
            coin = random.randint(0, self._range)
            sensor_value = self._alarm if coin != 0 else not self._alarm
            yield sensor_value


def iterate_forever():
    sensor = Sensor()
    ticks = 0
    for x in sensor.get():
        if x:
            logging.error(">>>>>>> R U N !!!!! <<<<<")
            # now reset the sensor
            sensor._reset()
        else:
            logging.debug("Sample: %d -- all systems are normal", ticks)
        ticks += 1
        if ticks & 100 == 0:
            sensor._detect_leak()
        time.sleep(1)


def get_n_samples(sensor, num):
    """ Samples the cheap sensor and returns ```num``` values

    :param sensor: the sensor to sample
    :type sensor: Sensor
    :param num: the number of samples to return, default 1,000
    :return: the list of samples
    :rtype: list of bool
    """
    count = num
    samples = []
    for x in sensor.get():
        samples.append(x)
        if count <= 0:
            break
        count -= 1
    return samples


def should_run(sensors=3, samples=1000, faulty=1.0):
    """ Finds out if we had a radioactive leak

    We define a leak if more than half the sensors return an alarm, for more than three
    consecutive samplings.

    Naive implementation, samples the sensors and assumes they will all fit in memory.

    :return: whether the sensor is faulty
    :rtype: bool
    """
    num = sensors
    sensors = [Sensor(faulty_pct=faulty) for _ in range(0, num)]
    samples = [get_n_samples(s, num=samples) for s in sensors]
    tot_count = len(samples[0])
    for x in xrange(0, tot_count):
        count = 0
        for i in range(num):
            if samples[i][x]:
                count += 1
        if count > 0:
            logging.error("At sample %d, %s sensors were in the ALARM state", x, count)
            if count > num / 2:
                break
    # Just because I wanted to show the use of for/else - a very Pythonic pattern!
    else:
        return False
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensors', required=True, type=int,
                        help="Number of sensors to activate")
    parser.add_argument('--samples', required=False, default=100, type=int,
                        help="Number of samples per sensor")
    parser.add_argument('--faulty-pct', default=5, help="The % failure rate of sensors", type=float)
    parser.add_argument('--test', default=False, help="Is this a test run?", type=bool)
    return parser.parse_args()


def main():
    conf = parse_args()
    if not conf.test:
        print("You should {}run".format("" if should_run(sensors=conf.sensors,
                                                         samples=conf.samples,
                                                         faulty=conf.faulty_pct)
                                        else "not "))
    else:
        iterate_forever()

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    main()
