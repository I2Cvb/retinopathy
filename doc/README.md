README.md
=========

Documentation of different types are generated in a scientific project.
These types can include articles for publications, code documentation, experiments' log, notes, etc.

This project uses latex for article publications and [Sphinx] for project and code documentation.

Structure
---------
```
doc                             # Documentation entry directory
├── build                       # Sphinx documentation output
│   ├── doctrees                # Sphinx internals
│   └── html                    # HTML rendered documentation output
│       └── index.html          # Project documentation ENTRY point 
├── Makefile                    # Makefile to run Sphinx
├── paperName                   # paper directory for article paperName 
│   ├── Makefile                # article building Makefile (if applicable)
│   └── README.md               # paperNeme README                        
├── README.md                   # This document
└── source                      # place to store all the project documentation
    ├── all-about-me.rst        #                                
    ├── conf.py                 # Sphinx configuration file
    ├── index.rst               # Project documentation entry point (source) 
    ├── _static                 # Sphinx internals
    └── _templates              # Sphinx internals
```

Writing articles
=================

A single project can produce several articles, each of these should be based in the ``doc`` folder with a different name.
The internal structure of each article might vary. 

Documenting with Sphinx
=======================

This project documentation is intended to be done using [Sphinx]. 
Sphinx transforms [reStructureText Primer] files, which are a type of markup language, into beautiful html documentation. 

Sphinx allow to create documentation from ``.rst`` files, and from the code itself. 
This is helpful since code-related documentation can be embedded within the code and imported from the documentation files at will. 

Adapting the Template check-list
===============================

- [ ] To modify in ``./souce/config.py``
  - [ ] Rename rr-init by the appropriated project's name. (it appears more than once)
  - [ ] Rename Author1, Author2 ...
- [ ] modify ``./source/index.rst`` to have a project description
- [ ] add folders and ``.rst`` files at will in ``./source`` to create the documentation

Where to go from here
=====================

Open science is nothing but sharing what you do with the world. Therefore documentation should reach as much people as possible.
We recommend to link the project's documentation to [read the docs] platform. 
In this manner, documentation is up-to-date and shared with the people who is interested in your work.

Sharing is the easiest way to spread the word and get help.
As example, this template documentation can be accessed using **read the (freaking) docs** at rr-init.rtfd.org

More information in how to link the documentation within a Github project to **read the (freaking) docs** can be found [here].

[Sphinx]: http://sphinx-doc.org
[reStructureText Primer]: http://sphinx-doc.org/rest.html
[here]: http://dont-be-afraid-to-commit.readthedocs.org/en/latest/documentation.html
[read the docs]: https://readthedocs.org/
