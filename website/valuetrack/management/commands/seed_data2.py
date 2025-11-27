from django.core.management.base import BaseCommand
from faker import Faker
import random

from valuetrack.models import Supplier, Problem, Solution, SupplierSolution, SolutionProblem

class Command(BaseCommand):
    help = 'Seed the database with stock control–related Supplier, Problem, and Solution data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data
        SupplierSolution.objects.all().delete()
        SolutionProblem.objects.all().delete()
        Supplier.objects.all().delete()
        Problem.objects.all().delete()
        Solution.objects.all().delete()

        # Stock-related problems
        problem_titles = [
            "Low Inventory Levels",
            "Overstocked Warehouse",
            "Delayed Supplier Delivery",
            "Inaccurate Stock Counts",
            "Seasonal Demand Spike",
            "Untracked Returns",
            "Stockout of Key Item",
            "Manual Reorder Errors"
        ]

        problems = []
        for title in problem_titles:
            problem = Problem.objects.create(
                title=title,
                description=fake.paragraph(nb_sentences=3)
            )
            problems.append(problem)

        # Stock control solutions
        solution_names = [
            "Automated Reorder System",
            "Supplier Diversification",
            "Inventory Audit Workflow",
            "Barcode Scanning Integration",
            "Demand Forecasting Tool",
            "Return Tracking Module"
        ]

        solutions = []
        for name in solution_names:
            solution = Solution.objects.create(
                name=name,
                description=fake.text(max_nb_chars=200)
            )
            solutions.append(solution)

        # Create Suppliers
        suppliers = []
        for _ in range(5):
            supplier = Supplier.objects.create(name=fake.company())
            suppliers.append(supplier)

        # Link Suppliers to Solutions with supplier-specific descriptions
        for solution in solutions:
            offered_by = random.sample(suppliers, k=random.randint(1, 3))
            for supplier in offered_by:
                SupplierSolution.objects.create(
                    supplier=supplier,
                    solution=solution,
                    description=fake.sentence(nb_words=12)
                )

        # Link Solutions to Problems
        for solution in solutions:
            solves = random.sample(problems, k=random.randint(1, 4))
            for problem in solves:
                SolutionProblem.objects.create(solution=solution, problem=problem)

        self.stdout.write(self.style.SUCCESS('✅ Stock control–themed seed data created successfully.'))