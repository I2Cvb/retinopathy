OCT image classification
========================

#### Manifesto

Because *Human* is **perfectible** and **error-prone**, because *Science* should be **open** and **flow** and because *cogito ergo sum*.

#### Status

## Research target output

1. MICCAI OMIA Workshop 2015
1. Extended version

### Datasets susceptible to be used in this study


Project folder structure
------------------------

### Structure Description
```
    project
    |- data                  # raw and primary data, are not changed once created
    |  |- raw/               # raw data, will not be altered
    |  +- clean/             # cleaned data, will not be altered once created
    |
    |- doc/                  # documentation for the study
    |  |- miccai-2015-omia/  # manuscript for MICCAI OMIA Workshop 2015
    |  +- source/            # sphinx source
    |
    |- pipeline/             # The different pipeline used for the study
    |  +- feature-classification  # pipeline to perform the classification
    |  +- feature-denoising       # pipeline to denoise the image
    |  +- feature-detection	  # pipeline to compute the feature
    |  +- feature-extraction	  # pipeline to extract the feature (DR)
    |  +- feature-validation	  # pipeline to show the results
    |
    |- results               # all output from workflows and analyses
    |  |- figures/           # graphs, likely designated for manuscript figures
    |  +- pictures/          # diagrams, images, and other non-graph graphics
    |
    |- scratch/              # temporary files that can be safely deleted or lost
    |
    |- script/               # scripts used to run on the cluster
    |
    |- src/                  # any programmatic code
    |
    |- datapackage.json      # metadata for the (input and output) data files
    |- requirements.txt      # list of the required packages (see virtualenv)
    |
    |- LICENSE.md
    |- README.md             # the top level description of content
```

Todo
----

### General
- [?] Add sphinx documentation as project.io website
- [ ] Understand the influence of flatteining the image
- [ ] Understand the influence of cropping the image
- [ ] Understand the influence of the LBP rotation invariance
- [ ] Find the optimum number of words using the codebook for the given descriptor

### Coding

[rr-init repository]: https://github.com/massich/rr-init
[virtual environment post]: http://www.silverwareconsulting.com/index.cfm/2012/7/24/Getting-Started-with-virtualenv-and-virtualenvwrapper-in-Python
[mozilla marketplace testing]: https://github.com/mozilla/marketplace-tests
[command reference]:http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html

