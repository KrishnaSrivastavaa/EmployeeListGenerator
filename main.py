import csv
import logging
from configparser import ConfigParser
from datetime import datetime, date, timedelta  # Import 'date' class
from faker import Faker
import os

# Initialize logger
logging.basicConfig(filename='employee_generator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EmployeeGenerator:
    def __init__(self, config_file='config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

        self.fake = Faker()

        self.employee_data = []

    def generate_employee(self):
        try:
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            employee_id = self.fake.unique.random_number(digits=6)
            manager_name = self.fake.name()
            join_date = self.fake.date_this_decade()
            dob = self.fake.date_of_birth(tzinfo=None, minimum_age=22, maximum_age=60)

            # Convert 'dob' to datetime object for proper subtraction
            dob_datetime = datetime.combine(dob, datetime.min.time())
            
            age = (datetime.now() - dob_datetime).days // 365
            salary = self.fake.random_int(min=30000, max=150000, step=1000)
            department_name = self.fake.random_element(self.config['DEPARTMENTS']['names'].split(','))

            self.employee_data.append([first_name, last_name, employee_id, manager_name,
                                       join_date, dob, age, salary, department_name])
        except Exception as e:
            logging.error(f"Error generating employee: {e}")

    def generate_employees(self, count=100):
        for _ in range(count):
            self.generate_employee()

    def save_to_csv(self, filename='employees.csv'):
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Firstname", "Lastname", "Employee ID", "Employee Manager Name",
                                 "Join Date", "Date of Birth", "Employee Age", "Employee Salary", "Employee Department Name"])
                writer.writerows(self.employee_data)

            logging.info(f"Employee data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving employee data: {e}")

if __name__ == "__main__":
    try:
        generator = EmployeeGenerator()

        num_employees = int(generator.config['GENERATOR']['num_employees'])
        generator.generate_employees(count=num_employees)

        output_file = generator.config['GENERATOR']['output_file']
        generator.save_to_csv(filename=output_file)
    except Exception as e:
        logging.error(f"Error: {e}")
