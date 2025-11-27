from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    # other fields like contact info, etc.
    
    def __str__(self):
        return self.name

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Solution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    suppliers = models.ManyToManyField(Supplier, through='SupplierSolution')
    problems = models.ManyToManyField(Problem, through='SolutionProblem')

    def __str__(self):
        return self.name

class SupplierSolution(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)  # Supplier-specific explanation

    # optional metadata: price, availability, etc.

class SolutionProblem(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    # optional metadata: effectiveness, notes, etc.

class SolutionImpact(models.Model):
    AREA_CHOICES = [
        ('assets', 'Assets'),
        ('services', 'Services'),
        ('spend', 'Spend'),
        ('income', 'Income'),
        ('other', 'Other'),
    ]

    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    notes = models.TextField(blank=True, null=True)  # Optional explanation or context

    def __str__(self):
        return f"{self.solution.name} impacts {self.get_area_display()}"