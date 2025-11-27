from django.contrib import admin
from .models import Supplier, Problem, Solution, SupplierSolution, SolutionProblem, SolutionImpact 

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(SupplierSolution)
admin.site.register(SolutionProblem)
admin.site.register(SolutionImpact)

