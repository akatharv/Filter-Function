import csv
import sys
import logging
import unittest
from io import StringIO

SALARY_COLUMN = "customer_salary"
JOB_COLUMN = "customer_job_category"
NAME_COLUMN = "customer_name"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def filter_customers_from_reader(reader, job_category, min_salary):
    """
    Filters customers from a CSV reader based on job category and salary.
    """
    results = []

    for row in reader:
        try:
            salary = float(row[SALARY_COLUMN].replace("$", ""))
        except (ValueError, KeyError):
            logging.warning("Skipping row due to invalid salary")
            continue

        if salary <= min_salary:
            continue

        if job_category != "ALL" and row.get(JOB_COLUMN) != job_category:
            continue

        results.append(row.get(NAME_COLUMN))

    return results


def filter_customers(file_path, job_category, min_salary):
    """
    Reads CSV from file path and applies filtering.
    """
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            return filter_customers_from_reader(reader, job_category, min_salary)
    except FileNotFoundError:
        logging.error("CSV file not found")
        return []

def main():
    if len(sys.argv) != 4:
        logging.error("Usage: python filter_customers.py <csv_file> <job_category> <min_salary>")
        return

    file_path = sys.argv[1]
    job_category = sys.argv[2]

    try:
        min_salary = float(sys.argv[3])
    except ValueError:
        logging.error("Minimum salary must be a number")
        return

    customers = filter_customers(file_path, job_category, min_salary)

    for name in customers:
        print(name)

class TestFilterCustomers(unittest.TestCase):

    def setUp(self):
        self.csv_data = """customer_name,customer_job_category,customer_salary
Allison Hill,IT,$12475.99
Monica Herrera,IT,$9562.48
Jonathan White,Public Service,$11928.72
"""

        self.reader = csv.DictReader(StringIO(self.csv_data))

    def test_filter_all_jobs(self):
        result = filter_customers_from_reader(self.reader, "ALL", 10000)
        self.assertEqual(result, ["Allison Hill", "Jonathan White"])

    def test_filter_it_jobs_only(self):
        reader = csv.DictReader(StringIO(self.csv_data))
        result = filter_customers_from_reader(reader, "IT", 10000)
        self.assertEqual(result, ["Allison Hill"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        unittest.main()
