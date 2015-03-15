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


import logging
import unittest
from sensors import Sensor


FORMAT = '%(asctime)-15s %(message)s'


class SensorsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    def setUp(self):
        self.sensor = Sensor(faulty_pct=0.01)

    def test_sensor(self):
        self.assertFalse(self.sensor.get().next())
        self.sensor._detect_leak()
        self.assertTrue(self.sensor.get().next())

    def test_faulty_sensor(self):
        fs = Sensor(faulty_pct=99.99)
        self.assertTrue(fs.get().next())

    def test_faulty_50pct(self):
        fs = Sensor(faulty_pct=55.0)
        self.assertTrue(fs.get().next() or fs.get().next())

    def test_can_get_a_lot(self):
        for _ in xrange(100000):
            self.sensor.get().next()
