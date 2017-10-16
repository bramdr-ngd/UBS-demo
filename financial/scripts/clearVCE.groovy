
import com.ngdata.lily.util.DnaHBaseSchema;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;

HTable htable = new HTable(HBaseConfiguration.create(), "CUSTOMER");
Scan scan = new Scan();
ResultScanner scanner = htable.getScanner(scan);
for (Result result : scanner) {
    result.getRow();
    htable.delete(
            new Delete(result.getRow())
                    .deleteFamily(DnaHBaseSchema.DNA_CF_BATCH_BYTES)
                    .deleteFamily(DnaHBaseSchema.DNA_CF_SPEED_BYTES));
    println("Deleted " + Bytes.toStringBinary(result.getRow()));

}


