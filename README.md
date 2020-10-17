# Partition number generator
## What is this?
This is a python script based off of Mathologer's video: ["The hardest 'What comes next?' (Euler's pentagonal formula)"](https://youtu.be/iJ8pnCO0nTY). There he describes an algorithm to generate the partition number of an integer number. 
This is a python implementation of that exact algorithm.

## How do I use this?
To generate the first `n` partition numbers:
```python
>>> from partition_number_generator import partition_number_generator
>>> gen = generate_partition_numbers()
>>> for i in range(n):
>>>     print(f'{i}: {gen.nth_partition_number(i)}')
0: 0
1: 1
2: 2
3: 3
4: 5
5: 7
6: 11
7: 15
8: 22
9: 30
10: 42
.
.
.
```