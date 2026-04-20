import os
import csv
import json

# ------------------------------
# Task 1 — FileManager
# ------------------------------
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"File NOT found: {self.filename}")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


# ------------------------------
# Task 2 — DataLoader
# ------------------------------
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.students.append(row)

            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

    def preview(self, n=5):
        print(f"First {n} rows:")
        print("------------------------------")
        for s in self.students[:n]:
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
        print("------------------------------")


# ------------------------------
# Task 3 — DataAnalyser (Variant A)
# ------------------------------
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        gpas = []
        high = 0

        for s in self.students:
            try:
                gpa = float(s['GPA'])
                gpas.append(gpa)

                if gpa > 3.5:
                    high += 1

            except ValueError:
                print(f"Warning: bad GPA for {s['student_id']}")
                continue

        self.result = {
            "total_students": len(gpas),
            "average_gpa": round(sum(gpas)/len(gpas), 2),
            "max_gpa": max(gpas),
            "min_gpa": min(gpas),
            "high_performers": high
        }

        return self.result

    def print_results(self):
        print("------------------------------")
        print("GPA Analysis")
        print("------------------------------")

        print("Total students :", self.result["total_students"])
        print("Average GPA :", self.result["average_gpa"])
        print("Highest GPA :", self.result["max_gpa"])
        print("Lowest GPA :", self.result["min_gpa"])
        print("Students GPA>3.5 :", self.result["high_performers"])

        print("------------------------------")


# ------------------------------
# Task 4 — ResultSaver
# ------------------------------
class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)

            print(f"Result saved to {self.output_path}")

        except Exception as e:
            print("Error saving file:", e)

def lambda_operations(students):
    print("------------------------------")
    print("Lambda / Map / Filter")
    print("------------------------------")

    high_gpa = list(filter(lambda s: float(s['GPA']) > 3.8, students))
    print("Students with GPA > 3.8 :", len(high_gpa))

    gpa_values = list(map(lambda s: float(s['GPA']), students))
    print("GPA values (first 5) :", gpa_values[:5])

    print("------------------------------")


# ------------------------------
# Task 5 — MAIN
# ------------------------------
fm = FileManager('students.csv')

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader('students.csv')
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)
analyser.analyse()
analyser.print_results()
lambda_operations(dl.students)
saver = ResultSaver(analyser.result, 'output/result.json')
saver.save_json()
