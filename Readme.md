# CSV Customer Filter Assignment

This is updated Python program that has written by the feedback given by sir.

The program reads customer data from a CSV file and filters customers based on:
- Job category
- Minimum salary

Only the names of matching customers are printed.


## How it works

- The CSV file is read using Python’s `csv.DictReader`.
- Each row is processed one by one.
- A customer is selected only if:
  - The job category matches the input (or `ALL` is provided), and
  - The salary is greater than the given minimum salary.


