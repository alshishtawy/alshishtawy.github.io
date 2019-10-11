==========================================================================================
OnlineElastMan: Self-Trained Proactive Elasticity Manager for Cloud-Based Storage Services
==========================================================================================

:date: 2016-03-18
:modified: 2017-04-11
:tags: Elasticity, Open Source, Cloud Computing
:category: Projects
:slug: online-elastman
:summary: A self-trained procative elasticity manager for the Cloud

The pay-as-you-go pricing model and the illusion of unlimited resources in the Cloud initiate the idea to provision
services elastically. Elastic provisioning of services allocates/de-allocates resources dynamically in response to the
changes of the workload. It minimizes the service provisioning cost while maintaining the desired service level
objectives (SLOs). Model-predictive control is often used in building such elasticity controllers that dynamically
provision resources. However, they need to be trained, either online or offline, before making accurate scaling
decisions. The training process involves tedious and significant amount of work as well as some expertise, especially
when the model has many dimensions and the training granularity is fine, which is proved to be essential in order to
build an accurate elasticity controller.

OnlineElastMan is a self-trained proactive elasticity manager for cloud-based storage services. It automatically evolves
itself while serving the workload. Experiments using OnlineElastMan with Cassandra indicate that OnlineElastMan
continuously improves its provision accuracy, i.e., minimizing provisioning cost and SLO violations, under various
workload patterns.

Publications
============
- Y. Liu, D. Gureya, A. Al-Shishtawy, and V. Vlassov, **"OnlineElastMan: Self-Trained Proactive Elasticity Manager for
  Cloud-Based Storage Services, "** in Cluster Computing, ISSN 1573-7543, May 2017. |CC2017_doi| |CC2017_pdf|
  |CC2017_bib|
- Y. Liu, D. Gureya, A. Al-Shishtawy and V. Vlassov, **"OnlineElastMan: Self-Trained Proactive Elasticity Manager for
  Cloud-Based Storage Services,"** IEEE International Conference on Cloud and Autonomic Computing (ICCAC), Augsburg,
  2016, pp. 50-59. |ICCAC2016_doi| |ICCAC2016_pdf| |ICCAC2016_bib|


Source Code
===========
Github: `OnlineElastMan <https://github.com/gureya/OnlineElasticityManager>`_


.. |CC2017_doi| image:: {static}/images/doi.png
    :alt: 10.1007/s10586-017-0899-z
    :height: 1em
    :target: https://doi.org/10.1007/s10586-017-0899-z
.. |CC2017_pdf| image:: {static}/images/pdf.png
    :alt: pdf
    :height: 1em
    :target: {static}/pdfs/publications/CC2017_OnlineElastMan.pdf
.. |CC2017_bib| image:: {static}/images/bibtex.png
    :alt: bibtex
    :height: 1em
    :target: {static}/pdfs/publications/CC2017_OnlineElastMan.bib


.. |ICCAC2016_doi| image:: {static}/images/doi.png
    :alt: 10.1109/ICCAC.2016.11
    :height: 1em
    :target: http://dx.doi.org/10.1109/ICCAC.2016.11
.. |ICCAC2016_pdf| image:: {static}/images/pdf.png
    :alt: pdf
    :height: 1em
    :target: {static}/pdfs/publications/ICCAC2016_OnlineElastMan.pdf
.. |ICCAC2016_bib| image:: {static}/images/bibtex.png
    :alt: bibtex
    :height: 1em
    :target: {static}/pdfs/publications/ICCAC2016_OnlineElastMan.bib
