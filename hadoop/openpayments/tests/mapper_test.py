__author__ = 'marco'

import sys
import threading
import unittest


import mapper

class TestMapper(unittest.TestCase):

    def test_map(self):
        sys.stdout.write('"4401251","2013","09/30/2014","Merck Sharp & Dohme Corporation","Covered Recipient Physician",,,"474860","MICHELLE",,"CATENACCI",,"26900 CEDAR RD STE 220 SOUTH",,"BEACHWOOD","OH","44122","United States",,,"Medical Doctor","Allopathic & Osteopathic Physicians/ Obstetrics & Gynecology/ Reproductive Endocrinology","OH",,,,,"Covered",,,"GANIRELIX",,"FOLLISTIM AQ",,,"0052030161",,"0052032601"," "," "," "," "," ","Merck Sharp & Dohme Corporation","100000000053","NJ","United States","No","4.48","11/13/2013","1","In-kind items and services","Food and Beverage",,,,"No","No Third Party Payment",,"No",,,"No"')
        t = threading.Thread(target=mapper.map_mfg_amt)
        t.start()

