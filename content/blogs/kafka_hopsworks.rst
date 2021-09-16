================================================================================================
The Ultimate Guide to Using an External Python Kafka Client to Interact with a Hopsworks Cluster
================================================================================================

:date: 2021-09-16
:tags: Kafka, Spark, Hopsworks, Python, Stream Processing
:category: Guides
:slug: kafka-hopsworks
:summary: We illustrate how to configure and use the python Confluent Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.


In this guide, we illustrate how to configure and use the python Confluent Kafka client to interact externally with a Hopsworks cluster. This include how to publish (write) and subscribe to (read) streams of events and how to interact with the schema registry and use Avro for data serialization.

This tutorial was tested using Hopsworks version 2.2.


Prepare the Environment
=======================
We'll start by preparing the schema, creating a Kafka topic, and downloading security credentials that we'll need in this tutorial.

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

Give your topic a name. This will be used later in the code to identify the topic. Enter the desired number of partitions and replication degree. Select a schema and schema version to use with this topic. For this tutorial, use the values shown in the image below.

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

.. class:: terminal

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

.. class:: terminal

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

   pip install confluent_kafka requests fastavro toml

For plotting you might need the following packages depending on your environment:

.. code-block:: bash

   pip install matplotlib
   pip install pyqt5
   sudo apt install qt5-default

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
With all preparation work out of the way, we are now ready to securely send sensor events into our HopsWorks Kafka topic. Below is the code for the `avro_producer.py <https://github.com/alshishtawy/hopsworks-examples/blob/main/kafka/avro_producer.py>`_.

The code starts by defining an **``Event``** class. This is the class for the objects we want to push into Kafka. You can change this class to match your application. The **``event_to_dict``** is a helper function that returns a dictionary representation of an event object to be used by the Avro serializer. Note that the key names should match the field names defined in the schema and also the value types should match those in the schema.

The **``main()``** function loads the configuration file and initializes the schema registry client, Avro serializer, and the producer.
Then initializes a number of sensors to generate data and finally uses the producer to push the generated data into Kafka.

.. include:: code/kafka/avro_producer.py
   :code: python
   :start-line: 19


The program takes a number of optional command line arguments to control the execution. You can specify the location of the configuration file using the -c flag. You can use -e to control the number of events generated per sensor and -d for the delay between events per sensor. The -t flag is used to resume the generation of the time series from the specified time step. This is useful if you want to continue generating more events after the program finishes or stopped.

.. code-block:: bash

   python avro_producer.py --help

.. class:: terminal

::

   $ python avro_producer.py --help
   usage: avro_producer.py [-h] [-c CONFIG] [-t TIME] [-e EVENTS] [-d DELAY]

   Produces time series data from emulated sensors into a kafka topic hosted at a HopsWorks cluster.

   optional arguments:
     -h, --help            show this help message and exit
     -c CONFIG, --config CONFIG
                           Configuration file in toml format.
     -t TIME, --time TIME  Start time step for the time series generator. Used to resume generating
                           the time series after stopping the program.
     -e EVENTS, --events EVENTS
                           Number of events to generate per sensor. Negative for infinite number.
     -d DELAY, --delay DELAY
                           Delay between events in second. Can be float.




.. warning::
   There is a bug in the HopsWorks REST API implementation for the schema registry that causes an HTTP error code 415
   "Unsupported Media Type".

   The reason for this error is a mismatch of the content type sent between the client and the server.
   The Confluent schema registry client is sending the correct type which is **'application/vnd.schemaregistry.v1+json'**.
   While the Hopsworks REST API server is expecting content of type **'application/json'**.
   The bug is reported to the HopsWorks team and is expected to be fixed in upcoming releases after v2.2.

   The easiest workaround is to change the Confluent schema registry client to send content type 'application/json'.
   This should be OK if you are using Python virtualenv as this change will not affect other applications.

   Edit the file `schema_registry_client.py <https://github.com/confluentinc/confluent-kafka-python/blob/97f08fe107d259eff6f9c281a61d92e204d2935d/src/confluent_kafka/schema_registry/schema_registry_client.py#L165>`_
   in your local python install directory and search for the line with *'Content-Type'* (line 165 in confluent-kafka v1.7.0)
   and change it to:
   ``'Content-Type': "application/json"}``

   The location of the file depends on your Python installation. If you are using virtualenv it will look something like:
   ``~/.virtualenvs/myvenv/lib/python3.8/site-packages/confluent_kafka/schema_registry/schema_registry_client.py``


Now lets generate some events. Below is a sample execution of 5 events with 0.5 seconds delay:

.. code-block:: bash

   python avro_producer.py -e 5 -d 0.5

.. class:: terminal

::

   $ python avro_producer.py -e 5 -d 0.5
   Producing sensor events to topic temperature.
   Press Ctrl-c to exit.
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 0
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 1
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 2
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 3
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 4
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 5
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 6
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 7
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 0
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 1
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 2
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 3
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 4
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 5
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 6
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 7
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 8
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 9
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 10
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 11
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 8
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 9
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 10
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 11
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 12
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 13
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 14
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 15
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 12
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 13
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 14
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 15
   Flushing records...
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 16
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 17
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 18
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 19
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 16
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 17
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 18
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 19
   To continue execution start from event 5


Let's generate some more events. Notice the last line in the execution above. It prints the time step that should be used to continue execution. To do that, we add ``-t 5`` to the command:

.. code-block:: bash

   python avro_producer.py -e 5 -d 0.5 -t 5

.. class:: terminal

::

   $ python avro_producer.py -e 5 -d 0.5 -t 5
   Producing sensor events to topic temperature.
   Press Ctrl-c to exit.
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 20
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 21
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 22
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 23
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 24
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 25
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 26
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 27
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 20
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 21
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 22
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 23
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 24
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 25
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 26
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 27
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 28
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 29
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 30
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 31
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 28
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 29
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 30
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 31
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 32
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 33
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 34
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 35
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 32
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 33
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 34
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 35
   Flushing records...
   Sensor Event b'sensor0' successfully produced to temperature [0] at offset 36
   Sensor Event b'sensor1' successfully produced to temperature [0] at offset 37
   Sensor Event b'sensor2' successfully produced to temperature [0] at offset 38
   Sensor Event b'sensor3' successfully produced to temperature [0] at offset 39
   Sensor Event b'sensor4' successfully produced to temperature [1] at offset 36
   Sensor Event b'sensor5' successfully produced to temperature [1] at offset 37
   Sensor Event b'sensor6' successfully produced to temperature [1] at offset 38
   Sensor Event b'sensor7' successfully produced to temperature [1] at offset 39
   To continue execution start from event 10


.. note::

   Remember that when we created the 'temperature' topic we set the number of partitions to two.
   In the output sample the partition number is shown in the square brackets after the topic name. For example 'temperature [0]'.
   This means that the event was successfully sent to the temperature topic at partition 0.

   Notice that events from the same sensor (e.g., sensor5) always ends up in the same partition (partition [1] in case of sensor5).
   This is enforced by Kafka to guarantee the ordered processing of events per event source.
   This is implemented using the **key** of the produced event which in our case is the sensor id.
   So pay attention to what you choose as the key depending on the application.



Avro Consumer
-------------

The Avro consumer code is similar to the producer code in previous section. It starts with the **``Event``** class which is the same
as the one in the producer code. The rest is similar but works in the other direction. So now we have a **``dict_to_event``** helper function that will return an event object and in the **``main()``** function we'll initialize an Avro deserializer and a consumer. Finally the code loops to poll messages and plot the values.

.. include:: code/kafka/avro_consumer.py
   :code: python
   :start-line: 19


Run ``avro_consumer.py`` with the command below. It will start receiving and plotting the 10 events we produced in the previous example. After that the program will wait for more events. Keep it running as we'll be producing more events soon.

.. note::

   The consumer received the 10 events we generated in the previous section because we set the ``auto.offset.reset`` property to ``'earliest'`` in our configuration file. This causes a consumer group, when first created, to get all available events in the Kafka topic. Another option is ``'latest'`` which will cause the consumer group to get only the current events ignoring old ones. Read more about consumer groups and offset management `here <https://docs.confluent.io/platform/current/clients/consumer.html>`_.

.. code-block:: bash

   $ python avro_consumer.py

.. class:: terminal

::

   $ python avro_consumer.py
   Event record sensor4: id: sensor4
           timestamp: 2021-09-16 18:32:45
           value: 73.43209881486389

   Event record sensor5: id: sensor5
           timestamp: 2021-09-16 18:32:45
           value: 53.20542290369634

   Event record sensor6: id: sensor6
           timestamp: 2021-09-16 18:32:45
           value: -1.6974040527855028

   Event record sensor7: id: sensor7
           timestamp: 2021-09-16 18:32:45
           value: 34.33728468834174

   Event record sensor4: id: sensor4
           timestamp: 2021-09-16 18:32:46
           value: 73.99429517973576

   Event record sensor5: id: sensor5
           timestamp: 2021-09-16 18:32:46
           value: 46.444456025618216
   ...



Keep the ``avro_producer.py`` running and try generating 20 more events with the command below.

.. code-block:: bash

   $ python avro_producer.py -e 20 -d 0.5 -t 10

The producer will start producing more events and you will see the consumer receiving and plotting them. The output should be similar to the figure below.

.. image:: {static}/images/kafka/kafka_prod_one_cons.png
    :alt: Kafka example with one consumer
    :width: 100%
    :align: center

Now try creating another ``avro_consumer.py`` in another terminal leaving the previous one running.

.. code-block:: bash

   $ python avro_consumer.py

Then produce 20 more events:

.. code-block:: bash

   $ python avro_producer.py -e 20 -d 0.5 -t 30

Notice that now the produced events will be split between the two consumers, or to be more precise, the partitions will be split among the available consumers. Since we created two partitions, we can have a maximum of two consumers. The output should look similar to the image below.

.. image:: {static}/images/kafka/kafka_prod_two_cons.png
    :alt: Kafka example with two consumers
    :width: 100%
    :align: center

.. note::

   Kafka remembers the events consumed by a consumer group. So if a consumer is interrupted and then restarted, it will continue from where it stopped. This is achieved through the consumer **commit** the offsets corresponding to the messages it has read. This can be configured to provide different delivery guarantees. The default is **auto-commit** that gives you **at least once** delivery guarantee. You can read more about this topic `here <https://docs.confluent.io/platform/current/clients/consumer.html>`_.


Source Code
===========
All source code is available at `Kafka HopsWorks Examples at GitHub`_

.. _Kafka Hopsworks Examples at GitHub: https://github.com/alshishtawy/hopsworks-examples/tree/main/kafka

.. _schema_management:
  https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/kafka.html#schema-management


..
  https://pythonhosted.org/sphinxjp.themes.basicstrap/sample.html#admonitions-docutils-origin
