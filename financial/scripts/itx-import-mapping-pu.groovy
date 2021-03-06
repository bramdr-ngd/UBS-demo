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

// id;itxseq;date;time;goal;subgoal;paymentType;channel;amount;

    parts = line.split(Pattern.quote(";"))
    partsCount = parts.length

    // an interaction should have at minimum a customer id & timestamp info. If not, the interaction is ignored
    if(partsCount>=4) {
        customer = partsCount > 1 ? parts[0] : ""
        datestring = partsCount > 2 ? parts[2] : ""
        timestring = partsCount > 3 ? parts[3] : ""
        goal = partsCount > 4 ? parts[4] : ""
        subgoal = partsCount > 5 ? parts[5] : ""
        paymentType = partsCount > 6 ? parts[6] : ""
        channel = partsCount > 7 ? parts[7] : ""
        amount = partsCount > 8 ? parts[8].trim() : "0"
        amount = amount != "" ? amount : "0"

        def dateParser = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")

        builder = new SafeGenericRecordBuilder(schema)

        builder.set("timestamp", dateParser.parse(datestring + " " + timestring).getTime())
        builder.set("customerId", customer)
        builder.set("goal", goal)
        builder.set("channel", channel)
        builder.set("subgoal", subgoal)
        builder.set("amount", Double.parseDouble(amount))
        builder.set("paymentType", paymentType)

        builder.build()
    }


}
