=======================================================
Traffic Flow Analysis with Spark: Getting Started Guide
=======================================================

:date: 2017-10-13
:modified: 2017-10-13
:tags: Spark, Big Data, Traffic Flow, Analytics, Jupyter
:category: Guides
:slug: traffic-flow-analysis
:summary: A guide that helps you get started with traffic flow analysis using Spark



.. image:: {static}/images/traffic_flow.png
    :alt: Traffic Flow Analysis
    :width: 90%
    :align: center

This guide will help you get started with traffic flow analysis of sensor data from Motorway Control Systems (MCS) using Spark.

To get started, download the Jupyter Notebook and the sample data from the links below. Run the Notebook in Jupyter and follow it step by step as it walks you through the basic stages of data analytics.

You can view a static version of the notebook here: `Traffic Flow Analysis (Static Version) <{static}/static/Traffic_Flow_Analysis/Traffic_Flow_Analysis_with_Spark.html>`_


Setting Up a Working Environment
================================

If you don't have access to a Spark and/or Jupyter installation. You can quickly get it up and running using Docker. We recommend using this `Spark Docker image`_ that contains all the tools we need. Including, Spark, Jupyter, Python, Scala, and much more.

Follow these steps:

1. Install Docker
2. Create a folder (e.g., /home/myuser/work) and copy the Notebook and unzipped sample data folder there
3. Run docker with the following command (**replace**  /home/myuser/work with your folder)

.. code-block:: bash

    docker run -it --rm -p 8888:8888 --name mySpark -v /home/myuser/work:/home/jovyan/work jupyter/all-spark-notebook

This should start Spark and Jupyter. Take note of the authentication token included in the Jupyter startup log messages. Use this url in your browser to access Jupyter.

.. _`Spark Docker image`: https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

Resources
=========
- `Traffic Flow Analysis Jupyter Notebook <{static}/static/Traffic_Flow_Analysis/Traffic_Flow_Analysis_with_Spark.ipynb>`_
- `Sample Data <{static}/static/Traffic_Flow_Analysis/data.zip>`_


