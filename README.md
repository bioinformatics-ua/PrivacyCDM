# PrivacyCDM - Privacy Preserving Techniques Applied to OMOP CDM

This repository contains the implementation of privacy-preserving techniques applied to the Observational Medical Outcomes Partnership (OMOP) Common Data Model (CDM). Specifically, this repository includes implementations of K-anonymity and L-diversity.

## Background

OMOP CDM is a widely used data model for observational medical research. It provides a standardized framework for organizing and analyzing data from electronic health records and other healthcare data sources. However, the use of such data for research purposes raises significant privacy concerns, as it often contains sensitive information about patients.

Privacy-preserving techniques aim to mitigate these concerns by allowing the analysis of sensitive data while ensuring the privacy of individuals. This repository provides implementations of such techniques that can be applied to OMOP CDM.

## Techniques Implemented

This repository currently implements the following privacy-preserving techniques:

- k-Anonymity: A technique that protects privacy by ensuring that each individual in a dataset is indistinguishable from at least K-1 other individuals.
- l-Diversity: A technique that ensures that sensitive information about individuals in a dataset is not overly concentrated in any particular group of individuals.

## Getting Started

To get started with using the privacy-preserving techniques implemented in this repository, please follow the instructions in the individual technique folders.

## Contributing

Contributions to this repository are welcome. If you find a bug, have a feature request or would like to contribute an implementation of a new technique, please open an issue or a pull request.
