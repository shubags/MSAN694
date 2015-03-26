package com.alertavert.demos;

import org.apache.commons.csv.CSVRecord;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class TokenizerMapperTest {

    TokenizerMapper mapper = new TokenizerMapper();

    @Test
    public void testParseLine() throws Exception {
        String line = "\"a, comma, field\",2,\"and, me\"";
        CSVRecord actual = mapper.parseLine(line);

        assertEquals(3, actual.size());
        assertEquals("a, comma, field", actual.get(0));
        assertEquals("2", actual.get(1));
        assertEquals("and, me", actual.get(2));
    }

    @Test
    public void testParseLineWithSpaces() throws Exception {
        String line = "\"Evil Corp, Inc.\", 2000 , \"Broken Wings, and Prayers\"   ";
        CSVRecord actual = mapper.parseLine(line);

        assertEquals(3, actual.size());
        assertEquals("Evil Corp, Inc.", actual.get(0));
        assertEquals("2000", actual.get(1));
        assertEquals("Broken Wings, and Prayers", actual.get(2));
    }
}
