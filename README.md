# ai-search-toy-examples

This repository currently implements some strategies for constrained search (Constraint Satisfaction Problems -- CSP), as presented in Chapter 6 of the Russell and Norvig's  Artificial Intelligence book (3rd edition). Those implementations are part of the evaluation in the Artificial Intelligence graduation course of University of São Paulo, taught in the first semester of 2019 at the Institute of Mathematics and Computer Sciences (São Carlos - São Paulo - Brazil).

Proper documentation will be added gradually.

The performed experiments with the map coloring problem are registered in the folder `run/results`, and they can be replicated by simply running the script `run/csp_testcase.py`.

All the scripts were implemented in Python and require `numpy` and `matplotlib` for working.

** Observation: the repository contains a subfolder entitled classical search, which originally was intended to contain traditional heuristic and uninformed search algorithms (A*, for instance). However, due to time limitations, only the CSP approaches were actually implemented. Maybe in the future I will finish their implementation, offering a (hopefully) useful resource for new students interested in this kind of algorithms.

*Saulo Martiello Mastelini*

#### References:

*Stuart Russell and Peter Norvig. 2009. Artificial Intelligence: A Modern Approach (3rd ed.). Prentice Hall Press, Upper Saddle River, NJ, USA.*
