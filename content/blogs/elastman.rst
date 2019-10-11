=============================================================
ElastMan: Elasticity Manager for Elastic Cloud-Based Services
=============================================================

:date: 2013-09-09 10:00
:modified: 2015-03-16 10:00
:tags: Elasticity, Open Source, Cloud Computing
:category: Projects
:slug: elastman
:summary: Elasticity Manager for Elastic Cloud-Based Services

.. image:: {static}/images/ElastManLogo.png
    :alt: ElastMan logo
    :width: 25%
    :align: left

The increasing spread of elastic Cloud services, together with the pay-as-you-go pricing model of Cloud computing, has
led to the need of an elasticity controller. The controller automatically resizes an elastic service in response to
changes in workload, in order to meet Service Level Objectives (SLOs) at a reduced cost. However, variable performance
of Cloud Virtual Machines and nonlinearities in Cloud services, such as the diminishing reward of adding a service
instance with increasing the scale, complicates the controller design.

ElastMan is an elasticity controller for Elastic Cloud-based services. ElastMan combines feedforward and feedback
control. Feedforward control is used to respond to spikes in the workload by quickly resizing the service to meet SLOs
at a minimal cost. Feedback control is used to correct modeling errors and to handle diurnal workload. To address
nonlinearities, our design of ElastMan leverages the near-linear scalability of elastic Cloud services in order to
build a scale-independent model of the service.

We have evaluated ElastMan using the Voldemort key-value store running in an OpenStack Cloud environment. Our
evaluation shows the feasibility and effectiveness of our approach to automation of Cloud service elasticity.

Publications
============
- ElastMan: Elasticity Manager for Elastic Key-Value Stores in the Cloud, Ahmad Al-Shishtawy, Vladimir Vlassov.
  The ACM Cloud and Autonomic Computing Conference (CAC 2013), Miami, FL, USA,  August 5-9, 2013. |doi1|
- ElastMan: Autonomic Elasticity Manager for Cloud-Based Key-value Stores, Ahmad Al-Shishtawy, Vladimir Vlassov. The
  22nd ACM International Symposium on High-Performance Parallel and Distributed Computing (HPDC '13). ACM, New York,
  NY, USA, pp. 115-116. |doi2|


Source Code
===========
Github: `ElastMan <https://github.com/alshishtawy/ElastMan>`_


.. |doi1| image:: {static}/images/doi.png
    :alt: 10.1145/2494621.2494630
    :height: 14pt
    :target: http://dx.doi.org/10.1145/2494621.2494630

.. |doi2| image:: {static}/images/doi.png
    :alt: 10.1145/2462902.2462925
    :height: 14pt
    :target: http://doi.acm.org/10.1145/2462902.2462925
