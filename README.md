# CP-nets

Implemented as described in "_An empirical investigation of ceteris paribus learnability_" [1].

## Fields
  
* Preference learning  
* Answer set programming (ASP)  
* Computing optimal stable models of logic programs with preferences  

## Implementation Info

Learns acyclic conditional preference networks from noisy preferences.  
Calculates transparent entailment [1].  
User can create custom datasets by following the existing format.  
Can generate a random database with noise.

The value of -1 for a variable can mean "any prefered".

movieLens Dataset (<https://grouplens.org/datasets/movielens),> each of the 19 variables is a movie Genre. 0 and 1 are the binary variables but in this specific case 0 denotes that it's not part of that genre, and 1 denotes that it is.

## Practical Info

On/Off Graph Printing: `Line 588:learnCPnet.py`  
On/Off Debug Mode: `Line 589:learnCPnet.py`  
When creating a new dataset, how to encode Var1 prefered over Var2: `1 1,1 0` and `0 0,0 1`  
When creating a new dataset, how to encode Var2 prefered over Var3: `0 0 1,0 0 0` and `0 1 0,0 1 1`  

## General Info

Theory:

* <https://arxiv.org/pdf/1107.0023.pdf>
* <https://ourspace.uregina.ca/bitstream/handle/10294/7676/Alanazi_Eisa_200277152_PHD_CS_Spring2017.pdf>

Total of only 4 implementations:

* <https://github.com/potassco/asprin> (Python)
* <https://github.com/FabienLab/CPnets-McDiarmid> (Python)
* <https://github.com/nmattei/GenCPnet> (C++)
* <https://github.com/KathrynLaing/DQ-Pruning> (R)

[1] Michael, L., & Papageorgiou, E. (2013, June). An empirical investigation of ceteris paribus learnability. In Twenty-Third International Joint Conference on Artificial Intelligence.