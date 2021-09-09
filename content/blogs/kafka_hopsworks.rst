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
    :width: 100%
    :align: center

Then enter a **Schema Name** field for your schema and paste the schema itself in the **content** field.
To check that the syntax of the schema is correct, press the **Validate** button. If everything is OK proceed by pressing the **Create** button.

.. caution::
   For the schema to work correctly with standard external clients, such as the Confluent Avro Producer/Consumer, the name given in the "Schema Name" field and in the schema declaration **must be the same name**.
   Furthermore, if you use a name space in the schema declaration, e.g., ``"namespace": "se.ri.kafka.tutorial", "name": "sensor"``, then the "Schema Name" field should contain the full name, i.e., ``se.ri.kafka.tutorial.sensor``.


.. image:: {static}/images/kafka/avro_schema_new.png
    :alt: Registring a new Avro schema
    :width: 100%
    :align: center


Kafka Topic
-----------
Topics are a way to organize related events. A topic is like a buffer between event producers and event consumers. Events are durably stored in a topic and are not deleted after consumption. Events can be read as many times as needed and you define for how long Kafka should retain your events.

For scalability, a topic is divided into a number of partitions that are distributed across servers (called Kafka Brokers). Events are distributed among partitions either uniformly or by event key. Using an event key is recommended to guarantee that events from the same entity, e.g., user or sensor, end up in the same partition and thus processed in the correct order of arrival.

.. tip::
   The number of partitions determine the maximum parallelism for processing (consuming) events by a single application. You can have as many event producers per topic as you want. Also there can be as many applications processing (consuming) events from a topic as needed. But within a single application, also known as a **consumer group**, the maximum parallelism (number of consumers) is defined by the number of partitions in the topic. This restriction is to guarantee the ordered processing of events within a topic.

To create a new Kafka topic, open the topic settings in the Kafka tab and select *New Topic*.

.. image:: {static}/images/kafka/kafka_topic.png
    :alt: Kafka topics settings page
    :width: 100%
    :align: center

Give your topic a name. This will be used later in the code to identify the topic. Enter the desired number of partitions and replication degree. Select a schema and schema version to use with this topic.

.. note::
   For testing, it is OK to set the number of partitions and replicas to 1. In a production system, you should always set the number of replicas to larger that 1 (typically 3) to avoid data loss on server failures and also select appropriate number of partitions to achieve the desired performance based on the expected number and rate of events.

.. image:: {static}/images/kafka/kafka_topic_new.png
    :alt: Creating a new Kafka topic
    :width: 100%
    :align: center


Security Certificates
---------------------
Hopsworks provide a secure Kafka-as-a-Service. Connecting your Python Producers and Consumers from an external server to the one provided by Hopsworks requires exporting the project certificates. These are used by the clients to securely connect and authenticate against the Hopsworks Kafka cluster. The certificates are downloaded as a keystore and trustore. These are designed used by Java/Scala programs and needs to be converted to *.pem* format to be used by Python and other non Java programs.


To export your projects' certificates, go to *Project Settings* in the *Settings* tab and click *Export Certificates*.

.. image:: {static}/images/kafka/project_settings.png
    :alt: Project settings page
    :width: 100%
    :align: center

You will be asked to enter your login password before downloading.

.. image:: {static}/images/kafka/project_settings_export_1.png
    :alt: Exporting project certificates (1/2)
    :width: 100%
    :align: center

After successfully entering your password, two certificate files will be downloaded, trustStore.jks and keyStore.jks. The certificate password will be displayed. It's a long string that is similar to:
  ``MQJNW833YNBR9C0OZYGBGAB09P2PP4H5EHIALGWIT98I2PNSPTIXFCEI72FT0VLE``

.. important::
   Store these two files in a safe place as they give remote access to your project and data. Same goes for the password. Copy and save your password in a safe location as we'll need it later.



.. image:: {static}/images/kafka/project_settings_export_2.png
    :alt: Exporting project certificates (2/2)
    :width: 100%
    :align: center

Next, we'll convert the JKS keyStore into an intermediate PKCS#12 keyStore, then into PEM file.
You will be asked to enter a new password for each of the generated certificates and also the original certificate password you got from the previous step.

.. code-block:: bash

   $ keytool -importkeystore -srckeystore keyStore.jks \
      -destkeystore keyStore.p12 \
      -srcstoretype jks \
      -deststoretype pkcs12

.. container:: terminal

 ::

   $ keytool -importkeystore -srckeystore keyStore.jks -destkeystore keyStore.p12 -srcstoretype jks -deststoretype pkcs12
   Importing keystore keyStore.jks to keyStore.p12...
   Enter destination keystore password:
   Re-enter new password:
   Enter source keystore password:
   Entry for alias kafka_tutorial__meb10000 successfully imported.
   Import command completed:  1 entries successfully imported, 0 entries failed or cancelled

.. code-block:: bash

   $ openssl pkcs12 -in keyStore.p12 -out keyStore.pem

.. container:: terminal

 ::

   $ openssl pkcs12 -in keyStore.p12 -out keyStore.pem
   Enter Import Password:
   Enter PEM pass phrase:
   Verifying - Enter PEM pass phrase:
   $ ls
   keyStore.jks  keyStore.p12  keyStore.pem  trustStore.jks

We repeat the same steps for the trustStore.

.. code-block:: bash

   $ keytool -importkeystore -srckeystore trustStore.jks \
      -destkeystore trustStore.p12 \
      -srcstoretype jks \
      -deststoretype pkcs12


.. class:: terminal

::

    $ keytool -importkeystore -srckeystore trustStore.jks -destkeystore trustStore.p12 -srcstoretype jks -deststoretype pkcs12
    Importing keystore trustStore.jks to trustStore.p12...
    Enter destination keystore password:
    Re-enter new password:
    Enter source keystore password:
    Entry for alias hops_root_ca successfully imported.
    Import command completed:  1 entries successfully imported, 0 entries failed or cancelled

.. code-block:: bash

   $ openssl pkcs12 -in trustStore.p12 -out trustStore.pem

.. class:: terminal

::

   $ openssl pkcs12 -in trustStore.p12 -out trustStore.pem
   Enter Import Password:
   $ ls
   keyStore.jks  keyStore.p12  keyStore.pem  trustStore.jks  trustStore.p12  trustStore.pem

Now you should have ``keyStore.pem`` and ``trustStore.pem`` that we'll use in the rest of this tutorial. You can safely delete the intermediate ``.p12`` files.


API Key
-------
Hopsworks provides a rich `REST API <https://app.swaggerhub.com/apis-docs/logicalclocks/hopsworks-api>`_ to interact with most of the available services. One of these services is the *Schema Registry* that we'll be using in this tutorial. To access the *REST API* we'll need an *API Key*.

To create a new API Key associated with your account, open your user account settings.

.. image:: {static}/images/kafka/account_settings.png
    :alt: Account Settings
    :width: 100%
    :align: center


Select the API Keys tab. Give your key a name and select the services that the app using this key can access. Then click on *Create API Key*.

.. image:: {static}/images/kafka/account_settings_api_key_1.png
    :alt: Account Settings - API Keys tab
    :width: 100%
    :align: center

Copy and store your new key in a safe plase as this is the only time it will be displayed. If you loose your API Key you'll have to delete it and create a new one.

Your API Key will look somethin like this:

  ``K97n09yskcBuuFyO.scfQegUMhXfHg7v3Tpk8t6HIPUlmIP463BPdbTSdSEKAfo5AB8SIwY8LGgB4924B``

.. important::

   Store your API Key in a text file (e.g., apiKeyFile) next to your certificates. We'll use this file later to configure clients.

.. image:: {static}/images/kafka/account_settings_api_key_2.png
    :alt: Creating an API Key
    :width: 100%
    :align: center


Project Name and ID
-------------------

The final piece if information we need is the project name and ID. You will find this in your project settings tab.

.. image:: {static}/images/kafka/project_settings_name_id.png
    :alt: Project Name and ID
    :width: 100%
    :align: center



Avro Client
===========
Now we are ready for some coding. We'll create a Kafka Producer and Consumer using the standard confluent-kafka library and connect it to a Hopsworks cluster. You can find the source code for all examples at `Kafka Hopsworks Examples at GitHub`_.

You will need a working Python environment and the following packages:

.. code-block:: shell

   pip install confluent-kafka hops

..
   https://www.confluent.io/blog/avro-kafka-data/


Configuration File
------------------
We'll write down all the parameters we prepared in the previous section in a configuration file. This makes it easier to change and also to switch between multiple projects or deployments by switching configuration files.

Go through the parameters and change them accordingly to match your project settings. Then save it as `config.toml <https://github.com/alshishtawy/hopsworks-examples/blob/main/kafka/config.toml>`_

.. code-block:: toml

   [hops]
   url = '127.0.0.1'

   # for testing only! set this flag to false or path to server certificate file
   # needed when testing Hopsworks with a self signed certificate
   # otherwise leave this true
   verify = false

   [project]
   name =  'Kafka_Tutorial'
   id = '1143'
   ca_file = 'cert/trustStore.pem'
   certificate_file = 'cert/keyStore.pem'
   key_file = 'cert/keyStore.pem'
   key_password = 'asdf123'

   [kafka]
   topic = 'temperature'
   schema = 'sensor'
   port = '9092'

   [kafka.consumer]
   group_id = 'TutorialGroup'
   auto_offset_reset =  'earliest'

   [api]
   base = '/hopsworks-api/api'
   key = 'K97n09yskcBuuFyO.scfQegUMhXfHg7v3Tpk8t6HIPUlmIP463BPdbTSdSEKAfo5AB8SIwY8LGgB4924B'
   key_file = 'cert/apiKeyFile'



Sensor Data
-----------
We'll need some data to test our example. For that we'll generate a time series with trend, seasonality, and noise. The code can emulate multiple sensors. The generated data looks like the plot below.

.. image:: {static}/images/kafka/sensor_data_sample.png
    :alt: Sensor Data Sample
    :width: 100%
    :align: center


The code below for `sensor.py <https://github.com/alshishtawy/hopsworks-examples/blob/main/kafka/sensor.py>`_ generates the data.
The code was inspired by `this example <https://github.com/tensorflow/examples/blob/master/courses/udacity_intro_to_tensorflow_for_deep_learning/l08c01_common_patterns.ipynb>`_.
You can test it yourself by executing the file.

.. code-block:: bash

   $ python sensor.py

.. include:: code/kafka/sensor.py
   :code: python


Avro Producer
-------------
With all preparation work out of the way, we are now ready to securely send sensor events into our HopsWorks Kafka topic. Below is the code for `avro_producer.py <https://github.com/alshishtawy/hopsworks-examples/blob/main/kafka/avro_producer.py>`_.

.. include:: code/kafka/avro_producer.py
   :code: python
   :start-line: 19



Avro Consumer
-------------

.. include:: code/kafka/avro_consumer.py
   :code: python
   :start-line: 19



Source Code
===========
All source code is available at `Kafka HopsWorks Examples at GitHub`_

.. _Kafka Hopsworks Examples at GitHub: https://github.com/alshishtawy/hopsworks-examples/tree/main/kafka

.. _schema_management:
  https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/kafka.html#schema-management


..
  https://pythonhosted.org/sphinxjp.themes.basicstrap/sample.html#admonitions-docutils-origin
