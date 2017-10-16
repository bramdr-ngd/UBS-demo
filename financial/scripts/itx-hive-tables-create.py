#!/usr/bin/env python

from string import Template

# This script just outputs the commands to create the required tables.
# You should pipe it through | beeline -u jdbc:hive2://localhost:10000/default

#config
interaction_types= {'itx_atm': 'ngdata.lily.atm', 'itx_web': 'ngdata.lily.web' }

#Drop Tables
src = Template( """
DROP TABLE ${table_name}_augmented;
DROP TABLE ${table_name}_mapped;
""" )

for table_name, interaction_name in interaction_types.iteritems():
    d={
        'table_name': table_name,
    }
    #do the substitution
    result = src.substitute(d)
    print result



#Create Table
src = Template( """
CREATE external TABLE ${table_name}_${type}
  PARTITIONED BY (year string,month string,day string)
  ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
  STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
  OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
  LOCATION '/lily/interactions/default/${type}/${interaction_path}'
  TBLPROPERTIES (
    'avro.schema.url'='hdfs:/lily/interactions/default/${type}/${interaction_path}/.metadata/schema.avsc');
""" )

for type in ['augmented', 'mapped']:
    for table_name, interaction_name in interaction_types.iteritems():
        d={
            'table_name':table_name,
            'interaction_path': interaction_name.replace('.','_'),
            'type': type
        }
        #do the substitution Mapped
        result = src.substitute(d)
        print result

#MSCK REPAIR
src = Template( """
MSCK REPAIR TABLE ${table_name}_augmented;
MSCK REPAIR TABLE ${table_name}_mapped;
""" )

for table_name, interaction_name in interaction_types.iteritems():
    d={
        'table_name':table_name
    }
    #do the substitution
    result = src.substitute(d)
    print result