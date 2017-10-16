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

// ID;ITX;DATUM;TIME;GOAL;SUBGOAL;CHANNEL;AMOUNT;

    parts = line.split(Pattern.quote(";"))
    partsCount = parts.length

    // an interaction should have at minimum a customer id & timestamp info. If not, the interaction is ignored
    if(partsCount>=4) {
        customer = partsCount > 1 ? parts[0] : ""
        datestring = partsCount > 2 ? parts[1] : ""
        timestring = partsCount > 3 ? parts[2] : ""



        def dateParser = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")

        builder = new SafeGenericRecordBuilder(schema)

        builder.set("timestamp", dateParser.parse(datestring + " " + timestring).getTime())
        builder.set("customerCRMId", customer)
        builder.set("locationname", parts[3])
        builder.set("latitude", Double.parseDouble(parts[4]))
        builder.set("longitude", Double.parseDouble(parts[5]))

        builder.build()
    }


}
