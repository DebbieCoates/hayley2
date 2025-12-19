import csv
from django.db import transaction
from valuetrack.models import Supplier, Problem, Solution, SupplierSolution, SolutionProblem

CSV_FILE = "testdata_five.csv"

@transaction.atomic
def run():
    with open(CSV_FILE, newline='', encoding='cp1252') as f:
        reader = csv.DictReader(f)

        for row in reader:
            supplier_name = row["Supplier"].strip()
            supplier_desc = row["SupplierSolution.description"].strip()
            solution_name = row["Solution.name"].strip()
            solution_desc = row["Solution.description"].strip()
            problem_title = row["Problem.title"].strip()

            supplier, _ = Supplier.objects.get_or_create(name=supplier_name)

            problem, _ = Problem.objects.get_or_create(
                title=problem_title,
                defaults={"description": problem_title}
            )

            solution, _ = Solution.objects.get_or_create(
                name=solution_name,
                defaults={"description": solution_desc}
            )

            SupplierSolution.objects.get_or_create(
                supplier=supplier,
                solution=solution,
                defaults={"description": supplier_desc}
            )

            SolutionProblem.objects.get_or_create(
                solution=solution,
                problem=problem
            )

    print("Import complete!")