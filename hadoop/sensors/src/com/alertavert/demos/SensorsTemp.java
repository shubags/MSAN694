package com.alertavert.demos;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;

import java.io.IOException;

/**
 * Main class to drive the Hadoop example
 *
 * Created by marco on 2/22/15.
 */
public class SensorsTemp {

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: hadoop jar sensors.jar <in.csv> <output dir>");
            System.err.println(String.format("Invalid arguments passed: %s", stringify(args)));
            System.exit(1);
        }
        JobConf conf = new JobConf(SensorsTemp.class);
        conf.setJobName("SensorsTemp");
        conf.setMapperClass(TokenizerMapper.class);
        conf.setReducerClass(AverageCpuLoadReducer.class);
        conf.setOutputKeyClass(FloatWritable.class);
        conf.setOutputValueClass(FloatWritable.class);
        FileInputFormat.addInputPath(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
    }

    private static String stringify(String[] args) {
        if (args.length == 0) return "None";
        StringBuilder sb = new StringBuilder();
        for (String s : args) {
            sb.append(s).append(", ");
        }
        sb.setLength(sb.length() - 2);
        return sb.toString();
    }

}
