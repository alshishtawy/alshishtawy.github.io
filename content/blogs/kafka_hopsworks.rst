================================================================================================
The Ultimate Guide on Using an External Python Kafka Client to interact with a Hopsworks Cluster
================================================================================================

:date: 2021-06-21
:tags: Kafka, Spark, Hopsworks, Python, Stream Processing
:category: Guides
:slug: kafka-hopsworks
:summary: We illustrate how to configure and use a python Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.


In this guide, we illustrate how to configure and use a python Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.

This tutorial was tested using Hopsworks version 2.2.


Prepare the Environment
=======================
We'll start by creating a Kafka topic and downloading security credintials that we'll need in this tutorial.

Avro Schema
-----------
Kafka treats data as blobs of bytes. It is your responsibility to pick a data format per topic and use it consistently across applications interacting with the topic. You are free to choose any format you prefer such as JSON or Protobuf. However, `Avro <http://avro.apache.org/docs/current/>`_ became the industry standard for data format to use with Kafka. Avro is an open source data serialization system that is used to exchange data between systems across programming languages.

Avro relies on schemas that are used when writing/reading data. To simplify the management of schemas, Confluent implemented a
`Schema Registry <https://docs.confluent.io/platform/current/schema-registry/index.html>`_ as a layer on top of Kafka. Hopsworks implements its own schema registry that is compatible with Confluent Schema Registry v5.3.1. Kafka clients can use the schema registry to validate and make sure that the correct data is written to or read from a kafka topic.

In this tutorial, we'll use temperature sensors as an example. Each sensor will have a unique **ID**, produce a temperature as its **value** at a specific **timestamp**. We'll create a generic sensor schema that can be used with sensors with similar pattern.
The code blow list the schema used in this tutorial.
For more details about declaring Avro schemas and supported data types, check the `Avro schemas <https://avro.apache.org/docs/current/spec.html#schemas>`_ documentation.


..
  hops `schema_management`_

.. code-block:: json

   {
     "type": "record",
     "name": "sensor",
     "fields": [
       {
         "name": "timestamp",
         "type": "long",
         "logicalType": "timestamp-millis"
       },
       {
         "name": "id",
         "type": "string"
       },
       {
         "name": "value",
         "type": "double"
       }
     ]
   }


To register the above schema in Hopsworks, open the schemas settings in the Kafka tab and select **New Avro Schema**

.. image:: {static}/images/kafka/avro_schema.png
    :alt: Avro schema settings page
    :width: 90%
    :align: center

Then enter a **Schema Name** field for your schema and paste the schema itself in the **content** field.
To check that the syntax of the schema is correct, press the **Validate** button. If everything is OK proceed by pressing the **Create** button.

.. caution::
   For the schema to work correctly with standard external clients, such as the Confluent Avro Producer/Consumer, the name given in the "Schema Name" field and in the schema declaration **must be the same name**.
   Furthermore, if you use a name space in the schema declaration, e.g., ``"namespace": "se.ri.kafka.tutorial", "name": "sensor"``, then the "Schema Name" field should contain the full name, i.e., ``se.ri.kafka.tutorial.sensor``.


.. image:: {static}/images/kafka/avro_schema_new.png
    :alt: Registring a new Avro schema
    :width: 90%
    :align: center


Kafka Topic
-----------

.. image:: {static}/images/kafka/kafka_topic.png
    :alt: Kafka topics settings page
    :width: 90%
    :align: center

.. image:: {static}/images/kafka/kafka_topic_new.png
    :alt: Creating a new Kafka topic
    :width: 90%
    :align: center


Security Certificates
---------------------

.. image:: {static}/images/kafka/project_settings.png
    :alt: Project settings page
    :width: 90%
    :align: center

.. image:: {static}/images/kafka/project_settings_export_1.png
    :alt: Exporting project certificates (1/2)
    :width: 90%
    :align: center

.. image:: {static}/images/kafka/project_settings_export_2.png
    :alt: Exporting project certificates (2/2)
    :width: 90%
    :align: center


API Key
-------

.. image:: {static}/images/kafka/account_settings.png
    :alt: Account Settings
    :width: 90%
    :align: center

.. image:: {static}/images/kafka/account_settings_api_key_1.png
    :alt: Account Settings - API Keys tab
    :width: 90%
    :align: center

.. image:: {static}/images/kafka/account_settings_api_key_2.png
    :alt: Creating an API Key
    :width: 90%
    :align: center



MQJNW833YNBR9C0OZYGBGAB09P2PP4H5EHIALGWIT98I2PNSPTIXFCEI72FT0VLE

API
K97n09yskcBuuFyO.scfQegUMhXfHg7v3Tpk8t6HIPUlmIP463BPdbTSdSEKAfo5AB8SIwY8LGgB4924B

.. code-block:: python

   import hops

   x = 5
   y = x + 5
   print(y)

.. note::
   This is an important note

.. image:: {static}/images/SpanEdge.png
    :alt: ElastMan logo
    :width: 90%
    :align: center



Source Code
===========
Github: `Kafka Hopsworks Examples <https://github.com/alshishtawy/hopsworks-examples/tree/main/kafka>`_



.. _schema_management:
  https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/kafka.html#schema-management


..
  https://pythonhosted.org/sphinxjp.themes.basicstrap/sample.html#admonitions-docutils-origin
