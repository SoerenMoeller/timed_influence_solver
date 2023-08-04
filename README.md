# Solver for the 'Calculus of Temporal Influence'

---

### Usage
Use the method `solve` from `solver/solver.py` to test the solver.  
It expects a set of statements. Following the notation of the paper, the format is:
```
VDS     tuple[str, tuple[float, float], tuple[float, float], tuple[float, float], str]
TVS     tuple[str, tuple[float, float], tuple[float, float], tuple[float, float]]
TDS     tuple[str, tuple[float, float], tuple[float, float]]                           
```

Additionally, a hypothesis has to be provided. It should also follow one of the previous patterns.  

There are two modes for proof search. Either, the proof is performed to reach a Der-Depth of a given `k` (as described in the paper),
or statements are build until the range of the hypothesis is overlapped.  
The modes can be switched with the boolean parameter `k_mode`. The `k` value can be adapted by using
it as a parameter as well.  

--- 

### CSV Files
To make data persistent, it can be saved in a csv-file. For that, each row represents a statement, following the already presented format.
An example can be seen in [example_csv](examples/example_csv.csv).

--- 

### Requirements 

`sympy` and `matplotlib` have to be installed. Both can be installed using pip.

```
pip3 install sympy
pip3 install matplotlib
```