package industries.media.interactions

import org.apache.avro.Schema
import org.apache.avro.generic.GenericRecordBuilder
import com.ngdata.lily.util.avro.SafeGenericRecordBuilder

import java.util.regex.Pattern

def mapLine(String line, Schema schema) {
    if (line.startsWith("#"))
        return null;

    if (line.startsWith("ID"))
        return null;

// ID;DATUM;TIME;GOAL;SUBGOAL;CHANNEL;AMOUNT;

    parts = line.split(Pattern.quote(";"))
    partsCount = parts.length

    // an interaction should have at minimum a customer id & timestamp info. If not, the interaction is ignored
    if(partsCount>=4) {
        customer = partsCount >= 1 ? parts[0] : ""
        datestring = partsCount >= 2 ? parts[1] : ""
        timestring = partsCount >= 3 ? parts[2] : ""
        goal = partsCount >= 4 ? parts[3] : ""
        subgoal = partsCount >= 5 ? parts[4] : ""
        channel = partsCount >= 6 ? parts[5] : ""

        def dateParser = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")

        builder = new SafeGenericRecordBuilder(schema)

        builder.set("timestamp", dateParser.parse(datestring + " " + timestring).getTime())
        builder.set("customerId", customer)
        builder.set("goal", goal)
        builder.set("channel", channel)
        builder.set("subgoal", subgoal)


        builder.build()
    }


}
