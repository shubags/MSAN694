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
import logging
import random


class Sensor(object):

    #: when the sensor detects radioactivity it will emit this value
    BROKEN_VALUE = -1

    def __init__(self):
        """ The dumbest sensor on Earth - returns a random value, or a ```fixed``` value.

        With a 50% chance (if ```fair``` is ```True```), its generator method with yield a random
        value, or a ```fixed``` value; the default fixed value is ```DOM_VALUE```

        :param fixed: the fixed value to return, randomly, one half of the time
        :type fixed: int
        :param fair: if ```True``` it will return ```fixed``` about 50% of the time; otherwise it
                     will return ```fixed``` much more often
        """
        self._alarm = False
        self._range = 100

    def _detect_leak(self):
        """ A radioactive leak will trigger this method
        """
        self._alarm = True

    def _reset(self):
        """ And we can manually reset the sensor, in case want to avoid bad press
        """
        self._alarm = False

    def get(self):
        """ Generator method for the sensor, returns an infinite stream of sensor readings

        :return: this is a generator method, yields the random value
        :rtype: Iterator
        """
        while True:
            # Around 10% of the time this sensor will misreport its readings - because top
            # management wanted to save money and, obviously, the radioactivity detectors seemed
            # the most reasonable place where to go cheapo
            coin = random.randint(0, 10)
            sensor_value = self._alarm if coin is not 0 else not self._alarm
            yield sensor_value


def iterate_forever():
    sensor = Sensor()
    ticks = 0
    for x in sensor.get():
        if x:
            logging.error(">>>>>>> R U N !!!!! <<<<<")
            break
        ticks += 1
        if ticks == 100:
            sensor._detect_leak()
        logging.debug("Sample: %d -- all systems are normal", ticks)


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


def should_run(sensors=3, samples=1000):
    """ Finds out if we had a radioactive leak

    We define a leak if more than half the sensors return an alarm, for more than three
    consecutive samplings.

    Naive implementation, samples the sensors and assumes they will all fit in memory.

    :return: whether the sensor is faulty
    :rtype: bool
    """
    num = sensors
    sensors = [Sensor() for _ in range(0, num)]
    samples = [get_n_samples(s, num=samples) for s in sensors]
    tot_count = len(samples[0])
    for x in xrange(0, tot_count):
        count = 0
        for i in range(num):
            if samples[i][x]:
                count += 1
        if count > num / 2:
            logging.error("At sample %d, %s sensors were in the ALARM state", x, count)
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
    parser.add_argument('--test', default=False, help="Is this a test run?", type=bool)
    return parser.parse_args()


def main():
    conf = parse_args()
    if not conf.test:
        print("You should {}run".format("" if should_run(sensors=conf.sensors, samples=conf.samples)
                                        else "not "))
    else:
        iterate_forever()

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    main()
