package com.alertavert.demos;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import java.io.IOException;
import java.text.ParseException;
import java.util.logging.Logger;

/**
 * Created by marco on 2/22/15.
 */
public class TokenizerMapper extends MapReduceBase implements
        Mapper<LongWritable, Text, FloatWritable, FloatWritable> {

    public static final Logger log = Logger.getLogger(TokenizerMapper.class.getName());

    /**
     * Scans each line of input, finds the highest CPU temp and returns it as the key, and the
     * average CPU load as the value
     *
     * Ignores all errors, as either logging or reporting is usually pointless at the scale that Hadoop runs at.
     *
     * @param offset from the start of the file; it won't be used
     * @param text  the string containing the timestamp, 6x core temperaturers, CPU load average (1, 5, 15 min)
     * @param outputCollector used to write the output of the map: (highest CPU temp, avg 1 min load)
     * @param reporter
     * @throws IOException
     */
    @Override
    public void map(LongWritable offset, Text text,
                    OutputCollector<FloatWritable, FloatWritable> outputCollector, Reporter reporter)
            throws IOException {
        String line = text.toString();
        String[] tokens = line.split(",");
        if (tokens.length == 10) {
            // Find the highest CPU temperature
            try {
                // we can safely use 0C as I'm positive my PC never froze (we're in California!)
                Float maxTemp = 0.0F;
                for (int i = 1; i < 7; ++i) {
                    Float temp = Float.parseFloat(tokens[i]);
                    if (temp > maxTemp) {
                        maxTemp = temp;
                    }
                }
                Float avgCpuLoad = Float.parseFloat(tokens[7]);
                log.fine(String.format("Writing out: %f, %f", maxTemp, avgCpuLoad));
                outputCollector.collect(new FloatWritable(maxTemp), new FloatWritable(avgCpuLoad));
            } catch (NumberFormatException ex) {
                // log and ignore
                log.severe("[ERROR} could not parse into a valid number: " + ex.getLocalizedMessage());
            }
        }
    }
}
