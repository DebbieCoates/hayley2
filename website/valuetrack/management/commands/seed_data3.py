from django.core.management.base import BaseCommand
from faker import Faker
import random

from valuetrack.models import Supplier, Problem, Solution, SupplierSolution, SolutionProblem

class Command(BaseCommand):
    help = 'Seed the database with garden-related Supplier, Problem, and Solution data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data
        SupplierSolution.objects.all().delete()
        SolutionProblem.objects.all().delete()
        Supplier.objects.all().delete()
        Problem.objects.all().delete()
        Solution.objects.all().delete()

        # Create Suppliers
        suppliers = []
        for _ in range(5):
            supplier = Supplier.objects.create(name=fake.company())
            suppliers.append(supplier)

        # Garden-related problems
        garden_problems = [
            "Overgrown Weeds and Brambles",
            "Patchy Lawn and Poor Drainage",
            "Pest Infestation (Slugs, Aphids, Moles)",
            "Seasonal Plant Loss and Frost Damage",
            "Inconsistent Watering Across Zones",
            "Tool Storage and Access Challenges",
            "Wildlife Disruption (Foxes, Rabbits)",
            "Time-Intensive Maintenance"
        ]

        problems = []
        for title in garden_problems:
            problem = Problem.objects.create(
                title=title,
                description=fake.paragraph(nb_sentences=3)
            )
            problems.append(problem)

        # Garden-related solutions
        garden_solutions = [
            "Automated Irrigation System",
            "Wildlife-Resistant Fencing",
            "Robotic Lawn Mower",
            "Garden Zoning and Pathway Planning",
            "Integrated Pest Control Service",
            "Seasonal Planting Calendar",
            "Smart Tool Shed with Inventory Tracking"
        ]

        solutions = []
        for name in garden_solutions:
            solution = Solution.objects.create(
                name=name,
                description=fake.text(max_nb_chars=200)
            )
            solutions.append(solution)

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

        self.stdout.write(self.style.SUCCESS('✅ Garden-focused seed data created successfully.'))