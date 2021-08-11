================================================================================================
The Ultimate Guide on Using an External Python Kafka Client to interact with a Hopsworks Cluster
================================================================================================

:date: 2021-06-21
:tags: Kafka, Spark, Hopsworks, Python, Stream Processing
:category: Guides
:slug: kafka-hopsworks
:summary: We illustrate how to configure and use a python Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.


In this guide, we illustrate how to configure and use a python Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.

Prepare the Environment
=======================
We'll start by creating a Kafka topic and downloadin security credintials that we'll need in this tutorial.

Avro Schema
-----------

.. image:: {static}/images/kafka/avro_schema.png
    :alt: Avro schema settings page
    :width: 90%
    :align: center

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
