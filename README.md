impweb
======

Web application to provide access to machine learning and other tools
for assisting with membrane protein expression

The code for score calculation is handled by other codes
(e.g. [clemlab/IMProve](https://github.com/clemlab/improve))


## Start workers with

```shell
FLASK_APP=webapp.py flask rq worker impweb-high impweb-med impweb-low
```

## TODO

* Run all from CLI

* output visualization
    * Table with outcomes
    * wrt nycomps, ecoli datasets
    * run Pfam and see if exists in NYCOMPS, prerun?
    * Button to download spreadsheet with features, score, names, and sequences

* Sanitization
    * Javascript input santization? -- minimum length
    * Accept uniprot id as input


* Methods
    * Would be cool to also provide scores from TMCrys method
    * Find protein homologs and then coding sequences (seems like a bit of work)
    * Recoding sequences (experimental)
    * Pointing in sequence space (experimental)

* REST API
    * __Should be__ fairly easy to finish up
