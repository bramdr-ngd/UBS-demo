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

    fields="id;date;time;goal;subgoal;channel;simulationType;simulationLoanAmount;simulationDownPayment;simulationMonthlyPayment;simulationPaymentRate;simulationDuration;simulationTradeInValue;simulationCashRebate;currentPageId".split(";");

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
        builder.set("customerCRMId", customer)
        builder.set("goal", goal)
        builder.set("channel", channel)
        builder.set("subgoal", subgoal)

        for (int i = 6; i < fields.length; i++) {
            builder.set(fields[i], convertType(parts[i], schema.getField(fields[i]).schema()));
        }

        builder.build()
    }
}

def convertType(Object value, Schema schema) {
    Object outValue = null;
    Schema.Type type = schema.getType()
    if (value == null || "null".equals(value.toString()) || type.equals(Schema.Type.NULL)) {
        return null;
    } else if (type.equals(Schema.Type.STRING)) {
        outValue = value
    } else if (type.equals(Schema.Type.LONG)) {
        outValue = Long.parseLong(value.toString())
    } else if (type.equals(Schema.Type.INT)) {
        outValue = Integer.parseInt(value.toString())
    } else if (type.equals(Schema.Type.FLOAT)) {
        outValue = Float.parseFloat(value.toString())
    } else if (type.equals(Schema.Type.DOUBLE)) {
        outValue = Double.parseDouble(value.toString())
    } else if (type.equals(Schema.Type.BOOLEAN)) {
        outValue = Boolean.valueOf(value.toString())
    } else if (type.equals(Schema.Type.UNION)) {
        Iterator typeIt = schema.getTypes().iterator()
        while (outValue == null && typeIt.hasNext()) {
            outValue = convertType(value, typeIt.next())
        }
    }
    return outValue;
}
