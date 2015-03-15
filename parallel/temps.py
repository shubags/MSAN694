__author__ = 'marco'

import os
import time


def profile(func):
    """Profiles a function, printing out the time it takes to execute

        Use as a decorator::

            @profile
            def my_func(x, y):
                # do something that takes time
                pass

    :param func: the function to execute
    :return: a wrapper function
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        unit = 'sec'
        if elapsed < 1:
            elapsed *= 1000
            unit = 'msec'
        print("[{func}] took {elapsed} {unit}".format(func=func.__name__, elapsed=elapsed, unit=unit))
        return r
    return wrapper


# FIXME: don't do this; use a CLI argument instead
SENSOR_DATA_FILE = '../hadoop/sensors/data/temperature.log.csv'


def get_cwd():
    """ Find the current, absolute path that this script is being executed from

    :return: the absolute path of the currently executing python script
    """
    return os.path.abspath(os.path.dirname(__file__))


def min_max(values):
    """ Returns a tuple with the min and max values contained in the iterable ```values```

    :param values: an iterable with comparable values
    :return: a tuple with the smallest and largest values (in this order)
    """
    min_ = None
    max_ = None
    for val in values:
        # Need to take care of the fact that None < (anything else)
        if not min_:
            min_ = val
        if val < min_:
            min_ = val
        if val > max_:
            max_ = val
    return min_, max_

@profile
def calc_max_cpu(records):
    """ Returns the CPU usage at the max temperature, ever

    :param records: a list of records of min, max temp and associated CPU avg load
    :return: a record with the highest recorded temperature, and the associated list of CPU loads
    """
    max_temp = 0
    cpu_loads = []
    for record in records:
        if record['max'] > max_temp:
            max_temp = record['max']
            cpu_loads = [100 * record['cpu']]
        elif record['max'] == max_temp:
            cpu_loads.append(100 * record['cpu'])
    return max_temp, cpu_loads


@profile
def read_records(data_file):
    data_points = []
    for l in open(data_file):
        line = l.strip()
        values = line.split(',')
        mi, mx = min_max([float(x) for x in values[1:7]])
        cpu = float(values[7])
        data_points.append({
            'min': mi,
            'max': mx,
            'cpu': cpu
        })
    return data_points


def main():
    data_file = os.path.join(get_cwd(), SENSOR_DATA_FILE)
    data_points = read_records(data_file)
    print("There are {} data records".format(len(data_points)))
    temp, cpu_values = calc_max_cpu(data_points)
    avg = reduce(lambda acc, x: acc + x, cpu_values) / len(cpu_values)
    print("The highest temperature was {temp}C at {avg}% average CPU load".format(temp=temp, avg=avg))


if __name__ == '__main__':
    main()
