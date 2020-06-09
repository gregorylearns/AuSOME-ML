# AUSOME Microsat

Demavivas, IG, Abrasaldo, GGA II, Fabilioren SR, Kim KE

## Disclaimer

The code will be very hard to read. We will continuously attempt to try and tidy it up. We are not experienced programmers. And for some of us, this was among our first large Python project.

Thank you for your patience.


## Background


This was a bioinformatics project during internship at the Philippine Genome Center during September - October 2019.

AUtomated Scoring of MicrosatellitEs using Machine Learning (AuSOMe-ML) aims to be a proof of concept towards the application of machine learning techniques in automating the scoring of microsatellite peaks. 

Microsatellites are non-coding bases in DNA that are usually 50-200 base pairs (bp) long. They are also known as Simple Sequence Repeats (SSRs) or Short Tandem Repeats (STR). They are unique to every individual organism due to errors in DNA replication and recombination. They are linked to about 14 neurological disorders. They are an important tool in fields such as forensics, population studies, and conservation genetics.

When these microsatellites are sequenced, they do not yield the usual ATGC permutation found in DNA, but since they all are composed of repeating subunits, they are detected as peaks.

These peaks have to be visually inspected and differentiated from distorting factors such as noise and stutters.

Several non-manual methods have been explored to help automate this manual task. An image based method was tested by Daniels et al on 1998. Fragman is an R package that is aimed for this problem. The package used peak threshold as the main basis for peak-calling.

This proof-of-concept was done using Applied Biosystems Inc FSA file formats.

The aim of this proof of concept were to create  a predictive model that will automate allele calling of microsatellite data.

### Data collection

Microsatellite data obtained from Hsc 40 loci of Holothuria scabra.

ABI 3730xl DNA Analyzer was used to sequence the fragments and export in ‘.fsa’ format

477 fsa files containing Channels 1, 2, 3, 4, and 105 (Ladder)

Hsc 40 loci contained in Channel 1 

### Machine Learning Model

Data was split 75-25 as training and testing datasets

Data was fitted into a Random Forest Classifier

5-fold cross validated using GridSearchCV to avoid overfitting.


## Dependencies

Install the dependencies by

```
$ pip3 install biopython \
	numpy \
	pandas \
	matplotlib \ 
	scikit-learn
```

Also the [findpeaks](https://github.com/jankoslavic/py-tools/blob/master/findpeaks/findpeaks.py) library by Janko Slavic.

