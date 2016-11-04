ml-website
==========

Website for machine learning and other tools developed.

The goal of this project would be to create a simple website that would accept
gene/protein sequence(s), perform a calculation on it, and return the result
in an appropriate format.

The code for the calculation is handled by smsaladi/ml-expression.

Ideally the build should be extensible and allow selecting among a set of
calculation interfaces as they are developed.

The backend will be written in Python using the Django framework. The frontend
will be constructed using React.js (maybe Ajax) stylized using Bootstrap.js.


## Risks:

Input sanitization. Ideally this would eventually be a public-facing website,
so having basic security precautions in place is necessary.


## TODO

* [ ] save inputs to sqlite

* [ ] error-logging
* [ ] email-sending when done (need another field)
* [ ] bokeh for visualization

* [ ] scheduler for cluster queue [torque]
* [ ] qsub/job submission

* [?] EMAIL OUT RESULTS
* [ ] FILE UPLOADING AND SENDING OF SEQUENCES
* [ ] HIGHER-UP SANITIZATION
* [ ] SUPPORT FOR ARBITRARY NUMBERS OF SEQUENCES

* [ ] passing an argument and returning between views - SEMI DONE

* [ ] figure out hosting situation


## Credits

Backend groundwork put together by @cynest for his CS 11 project
