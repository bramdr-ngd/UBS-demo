import java.nio.file.Paths;
import groovy.json.JsonSlurper;
import groovy.sql.Sql;
import org.apache.avro.Schema
import org.apache.avro.generic.GenericRecordBuilder
import com.ngdata.lily.util.avro.SafeGenericRecordBuilder
import com.ngdata.lily.itx.ingest.api.*
import com.ngdata.lily.itx.ItxTypeService;

import com.ngdata.lily.dna.entitytype.DnaEntityType


dnaEntityType = DnaEntityType.forName("customer")

ItxService itxService = lily.scopeTo(dnaEntityType).getService(ItxService.class);
ItxTypeService itxTypeService = lily.getService(ItxTypeService.class);
ItxIngester ingester = itxService.createIngester(ItxIngesterSettings.defaultSettings());

fileName = args[0]
parser = new JsonSlurper()
json = parser.parse(new FileReader(fileName));

schema = itxTypeService.getMappedSchema("lily.diagnostics.performance").get().getSchema();
thedate = Paths.get(fileName).getFileName().toString().subSequence(5,15)
println thedate

timestamp = org.joda.time.format.ISODateTimeFormat.date().parseMillis(thedate)

def db = [url:'jdbc:phoenix:localhost:2181', driver:'org.apache.phoenix.jdbc.PhoenixDriver']
def sql = Sql.newInstance(db.url,db.driver)

for ( dnaVar in json.DNA_VAR_DEFINITIONS) {
    def id =  com.ngdata.lily.dna.entitytype.SourceIdAlgorithm.MURMUR3.mapToDnaEntityId(dnaVar.name)
    def params = [
            id,
            '0',
            dnaVar.name,
            'customer',
            dnaVar.variableType,
            dnaVar.valueType.scalarType,
            dnaVar.attributes.label,
            dnaVar.attributes.category,
            dnaVar.attributes.subcategory,
            dnaVar.attributes.description,
            dnaVar.valueType.hasProperty('groups')
    ]
    sql.executeUpdate ('upsert into metric(id, tenant_id, metric_name, entity_type,  metric_type, metric_value_type, metric_label, metric_category, metric_subcategory, metric_description, metric_breaked) values (?,?,?,?,?,?,?,?,?,?,?)', params);
    sql.commit();
}
/*
println 'Some read what we wrote:'
 sql.eachRow('select * from METRIC') { row ->
     println "$row.metric_name ($row.metric_type)"
 }
*/


for (metric in json.QUERY_BENCHMARK.benchmarkRunResults) {
    metricName = metric.getKey()

    channel  = 'lily'
    goal = 'diagnostics'
    subgoal = 'performance'

    for (int i = 0; i < metric.getValue().size(); i++) {
        run = metric.getValue()
        seq = i

        builder = new SafeGenericRecordBuilder(schema)
        builder.set('timestamp', timestamp + i)
        builder.set('channel', channel)
        builder.set('goal', goal)
        builder.set('subgoal', subgoal)
        builder.set('sequence', seq)
        builder.set('metricName', metricName)
        builder.set('errorCount', (long)run[i].errorCount)
        builder.set('meanGroupsPerValue', (long) run[i].meanGroupsPerValue)
        builder.set('milliseconds', (long) run[i].milliseconds)
        builder.set('nonNullCount', (long) run[i].nonNullCount)
        builder.set('unknownCount', (long) run[i].unknownCount)

        ingester.addItx( builder.build() )
    }

}

ingester.close()
