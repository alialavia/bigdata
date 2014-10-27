This directory contains our interim report LATEX file (intermreport.tex), 
together with all of its bells and whistles, i.e. images, bibliography (report.bib) and so on.

You only need to work on the abovementioned files. In particular,
the directory use the LaTeX2e package for
Lecture Notes in Computer Science (LNCS) of Springer-Verlag.
The following files belong to the package and better to remain untouched:

  history.txt        the version history of the package

  llncs.cls          the LaTeX2e document class

  llncs.tex          the sample input file

  llncs.doc          the documentation of the class (LaTeX source)
  llncsdoc.pdf       the documentation of the class (PDF version)
  llncsdoc.sty       the modification of the class for the documentation
  llncs.ind          an external (faked) author index file
  subjidx.ind        subject index demo from the Springer book package
  llncs.dvi          the resultig DVI file (remember to use binary transfer!)

  sprmindx.sty       supplementary style file for MakeIndex
                     (usage: makeindex -s sprmindx.sty <yourfile.idx>)

  splncs03.bst       current LNCS BibTeX style with aphabetic sorting

  aliascnt.sty       part of the Oberdiek bundle; allows more control over
                     the counters associated to any numbered item
  remreset.sty       by David Carlisle
