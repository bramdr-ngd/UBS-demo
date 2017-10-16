import com.ngdata.lily.util.LilyConfiguration
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.hbase.Cell
import org.apache.hadoop.hbase.CellUtil
import org.apache.hadoop.hbase.client.Delete
import org.apache.hadoop.hbase.client.HTable
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.client.Scan
import org.apache.hadoop.hbase.util.Bytes

Configuration conf = LilyConfiguration.create();

HTable htable = new HTable(conf, "SYSTEM.CATALOG");

String[] tableNames = args

Scan scan = new Scan();
//scan.setRaw(true);

println "Performing deletes for " + tableNames

List<Delete> deletes = new ArrayList<>();

for (Result result in htable.getScanner(scan)) {
    for (Cell cell in result.rawCells()) {
        for (String tableName : tableNames) {
            String qualifiedTableName = (tableName.indexOf('.') >= 0) ? tableName : "."+tableName;
            String bytesTableName = qualifiedTableName.replace(".","\\x00");
            byte[] row = CellUtil.cloneRow(cell);
            if (Bytes.equals(row, Bytes.toBytesBinary("\\x00" + bytesTableName))) {
                deletes.add(new Delete(row))
            }
            if (Bytes.startsWith(row, Bytes.toBytesBinary("\\x00" + bytesTableName + "\\x00"))) {
                deletes.add(new Delete(row))
            }
        }
    }
}

println "Will perform the following deletes:"

for (Delete delete : deletes) {
    println delete
}

htable.delete(deletes);
htable.close();

println "Deletes performed."
