===========================================
HDFS Contents Manager for Jupyter Notebooks
===========================================

:date: 2017-08-07 11:00
:tags: Big Data, Open Source, Jupyter, HDFS
:category: Projects
:slug: hdfs-contents-manager

I implemented a contents manager for Jupyter_ notebooks that uses HDFS as a storage backend to store notebooks.
I have two versions. The main difference is the library used to read/write HDFS.

- The first version uses HDFS3_ which is based on libhdfs3, a native C/C++ library to interact with the Hadoop
  File System (HDFS).

- The second version uses Pydoop_ which is based on the official libhdfs_, a JNI based C API for Hadoop's Distributed
  File System (HDFS).

The HDFS Contents Manager is used to add Jupyter_ support to the Hops_ Big Data platform. Check out the `HDFS Contents
Manager poster`_ at the SICS Open House 2017 event for more details.


Source Code
===========
- The `HDFS3 version`_
- The `pydoop version`_


.. _HDFS3: https://github.com/dask/hdfs3
.. _Pydoop: http://crs4.github.io/pydoop/
.. _libhdfs: https://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-hdfs/LibHdfs.html
.. _HDFS3 version: https://github.com/alshishtawy/hdfscontents
.. _pydoop version: https://github.com/hopshadoop/hdfscontents
.. _Jupyter: http://jupyter.org/
.. _Hops: http://www.hops.io/
.. _`HDFS Contents Manager poster`: {static}/pdfs/posters/2017/HopsJupyter_V2.pdf