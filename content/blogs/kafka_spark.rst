===========
Spark it Up
===========

:date: 2021-10-06
:tags: Kafka, Spark, Hopsworks, Python, Stream Processing
:category: Guides
:slug: kafka-spark
:summary: We show how to use Spark and Jupyter notebooks to store, process, and visualize events in Kafka on Hopsworks.


In this guide, We show how to use Spark and Jupyter notebooks to store, process, and visualize events in Kafka on Hopsworks. This is **part two** in a series of tutorials looking into how to work with streaming events using the HopsWorks platform. The examples in this guid builds on the previous examples, so make sure to read `part one <{filename}./kafka_hopsworks.rst>`_ first.

This tutorial was tested using Hopsworks version 2.2.


Store Events Permanently
========================
We'll start by preparing the schema, creating a Kafka topic, and downloading security credentials that we'll need in this tutorial.

Read the `Kafka Spark Integration <https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html>`_ docs

.. note::

   For streaming queries, the ``startingOffsets`` only applies when a **new query** is started, and that resuming will always pick up from where the query left off. Newly discovered partitions during a query will start at earliest.


Source Code
===========
All source code is available at `Kafka HopsWorks Examples at GitHub`_

.. _Kafka Hopsworks Examples at GitHub: https://github.com/alshishtawy/hopsworks-examples/tree/main/kafka

..
  https://pythonhosted.org/sphinxjp.themes.basicstrap/sample.html#admonitions-docutils-origin
