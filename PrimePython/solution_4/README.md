# Python Prime Sieve by olliemath

![Algorithm](https://img.shields.io/badge/Algorithm-other-yellowgreen)
![Faithfulness](https://img.shields.io/badge/Faithful-yes-green)
![Parallelism](https://img.shields.io/badge/Parallel-no-green)
![Bit count](https://img.shields.io/badge/Bits-8-yellowgreen)

## Implementation Notes

In the *original* algorithm, we know that all even integers are divisible
by 2, so we take the shortcut of assigning an array half the size.
The sieve algorithm just marks multiples of primes in this smaller array
as not prime. The cost is some extra math when finding the address of an
integer in the array, which you can visualise as
```python
[3, 5, 7, 9, 11, 13, 15, 17, 19...]
```

Here we take this one step further, by eliminating every third element in
the array. So we run our sieve on a starting array that looks like
```python
[5, 7, 11, 13, 17, 19, 23, 25, 29, ...]
```
The corresponding math to find an integer's position in the array is much
more complex, but the smaller array size seems more optimal. We could continue
down this path by also eliminating multiples of 5. I'm unsure if what we gain
in reduced array size will be lost by the added complexity of the addressing math.

## Running with Python

Install Python: https://www.python.org/downloads/


```
cd path/to/sieve
python PrimePY.py
```

## Running with Pypy

Download and extract Pypy3: https://www.pypy.org/download.html


```
cd path/to/pypy
pypy3 path/to/sieve/PrimePY.py
```

## Command line arguments

 - `--limit=X`, `-l X`: set upper limit for calculating primes. Default is 1_000_000.
 - `--time=X`, `-t X`: set running time, in seconds. Default is 10.
 - `--show`, `-s`: output the found primes.

## Running tests

```
cd path/to/sieve
python -m unittest
```

# Results on my machine

Running on

 - AMD Ryzen 7 PRO 4750U 1.4 GHz, Ubuntu 64 bit
 - Python: 3.8.1 64 bit
 - PyPy: 7.3.5
 - g++: 9.3.0


Here we show our solution running under pypy. The corresponding cpython implementation is competative natively,
but seems to suffer a big (2-3x) performance hit in docker.


                                                          Single-threaded
┌───────┬────────────────┬──────────┬─────────────────┬────────┬──────────┬─────────┬───────────┬──────────┬──────┬───────────────┐
│ Index │ Implementation │ Solution │ Label           │ Passes │ Duration │ Threads │ Algorithm │ Faithful │ Bits │ Passes/Second │
├───────┼────────────────┼──────────┼─────────────────┼────────┼──────────┼─────────┼───────────┼──────────┼──────┼───────────────┤
│   1   │ PrimePython    │ 4        │ olliemath       │  8688  │ 5.00144  │    1    │   base    │   yes    │ 8    │  1737.10066   │
│   2   │ PrimePython    │ 3        │ emillynge_numpy │  7585  │ 5.00051  │    1    │   base    │    no    │ 8    │  1516.84413   │
│   3   │ PrimePython    │ 2        │ ssovest         │  2140  │ 5.00214  │    1    │   base    │   yes    │ 8    │   427.81673   │
│   4   │ PrimePython    │ 1        │ davepl          │   20   │ 5.09315  │    1    │   base    │   yes    │      │    3.92684    │
└───────┴────────────────┴──────────┴─────────────────┴────────┴──────────┴─────────┴───────────┴──────────┴──────┴───────────────┘

