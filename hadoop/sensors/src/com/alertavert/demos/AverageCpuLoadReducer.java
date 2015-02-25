package com.alertavert.demos;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;

import java.io.IOException;
import java.util.Iterator;

/**
 * Created by marco on 2/22/15.
 */
public class AverageCpuLoadReducer extends MapReduceBase implements
    Reducer<FloatWritable, FloatWritable, FloatWritable, FloatWritable> {
    @Override
    public void reduce(FloatWritable temp, Iterator<FloatWritable> cpuLoads,
                       OutputCollector<FloatWritable, FloatWritable> outputCollector, Reporter reporter)
            throws IOException {
        int count = 0;
        Float sum = 0.0F;
        while (cpuLoads.hasNext()) {
            sum += cpuLoads.next().get();
            count++;
        }
        if (count > 0) {
            outputCollector.collect(temp, new FloatWritable(sum / count));
        }
    }
}
