export const ruleTestData = {
    "connections": [
      {
        "Connection ID": "baa5c6d6-0191-1000-df8b-28f9b254c312",
        "Destination Processor ID": "baa54b56-0191-1000-2a30-c80ba7354bd3",
        "Destination Processor Name": "PutMongo",
        "Source Processor ID": "baa559ac-0191-1000-0d61-b9fcba30dde2",
        "Source Processor Name": "ConsumeKafka_2_6"
      }
    ],
    "processors": [
      {
        "ID": "baa559ac-0191-1000-0d61-b9fcba30dde2",
        "Name": "ConsumeKafka_2_6",
        "Position": {
          "x": 120.0,
          "y": 280.0
        },
        "Properties": {
          "Commit Offsets": "true",
          "Communications Timeout": "60 secs",
          "auto.offset.reset": "earliest",
          "aws.profile.name": null,
          "bootstrap.servers": "140.238.153.4:10000",
          "group.id": "test_group2",
          "header-name-regex": null,
          "honor-transactions": "true",
          "kerberos-credentials-service": null,
          "kerberos-user-service": null,
          "key-attribute-encoding": "utf-8",
          "key.deserializer": "org.apache.kafka.common.serialization.StringDeserializer",
          "max-uncommit-offset-wait": "1 secs",
          "max.poll.records": "10000",
          "message-demarcator": null,
          "message-header-encoding": "UTF-8",
          "sasl.kerberos.keytab": null,
          "sasl.kerberos.principal": null,
          "sasl.kerberos.service.name": null,
          "sasl.mechanism": "GSSAPI",
          "sasl.password": null,
          "sasl.token.auth": "false",
          "sasl.username": null,
          "security.protocol": "PLAINTEXT",
          "separate-by-key": "false",
          "ssl.context.service": null,
          "topic": "user1_device4",
          "topic_type": "names",
          "value.deserializer": "org.apache.kafka.common.serialization.StringDeserializer"
        },
        "Type": "org.apache.nifi.processors.kafka.pubsub.ConsumeKafka_2_6",
        "Version": 5
      },
      {
        "ID": "baa54b56-0191-1000-2a30-c80ba7354bd3",
        "Name": "PutMongo",
        "Position": {
          "x": 848.0,
          "y": 280.0
        },
        "Properties": {
          "Character Set": "UTF-8",
          "Mode": "insert",
          "Mongo Collection Name": "TEST_NIFI",
          "Mongo Database Name": "testdb",
          "Mongo URI": "mongodb://root:enCore1289%40@140.238.153.4:22000",
          "Update Query Key": null,
          "Upsert": "false",
          "Write Concern": "ACKNOWLEDGED",
          "mongo-client-service": null,
          "put-mongo-update-mode": "doc",
          "putmongo-update-query": null,
          "ssl-client-auth": "REQUIRED",
          "ssl-context-service": null
        },
        "Type": "org.apache.nifi.processors.mongodb.PutMongo",
        "Version": 4
      }
    ]
  };