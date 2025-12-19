from django.shortcuts import render
from django.db.models import Prefetch
from .models import Problem, Solution, SupplierSolution, SolutionProblem, Supplier, SolutionImpact


def index(request):
    return render(request, 'index.html')
    


def suppliers(request):
    query = request.GET.get("q", "").strip()

    base_qs = Supplier.objects.all()

    if query:
        base_qs = base_qs.filter(name__icontains=query)

    suppliers = base_qs.prefetch_related(
        Prefetch(
            'suppliersolution_set',
            queryset=SupplierSolution.objects.select_related('solution'),
            to_attr='solution_links'
        )
    )

    suppliers_count = suppliers.count()

    return render(request, 'suppliers.html', {
        'suppliers': suppliers,
        'suppliers_count': suppliers_count,
        'query': query,
    })
    
def solutions(request):
    solutions = Solution.objects.prefetch_related(
        Prefetch(
            'solutionproblem_set',
            queryset=SolutionProblem.objects.select_related('problem'),
            to_attr='problem_links'
        ),
        Prefetch(
            'suppliersolution_set',
            queryset=SupplierSolution.objects.select_related('supplier'),
            to_attr='supplier_links'
        )
    )

    solutions_count = solutions.count()

    return render(request, 'solutions.html', {
        'solutions': solutions,
        'solutions_count': solutions_count
    })
    
def problems(request):
    query = request.GET.get("q", "").strip()

    base_qs = Problem.objects.all()

    if query:
        base_qs = base_qs.filter(title__icontains=query)

    problems = base_qs.prefetch_related(
        Prefetch(
            'solutionproblem_set',
            queryset=SolutionProblem.objects.select_related('solution').prefetch_related(
                Prefetch(
                    'solution__suppliersolution_set',
                    queryset=SupplierSolution.objects.select_related('supplier'),
                    to_attr='supplier_links'
                )
            ),
            to_attr='solution_links'
        )
    )

    problems_count = problems.count()

    return render(request, 'problems.html', {
        'problems': problems,
        'problems_count': problems_count,
        'query': query,
    })
    
def supplier_detail(request, supplier_id):
    supplier = Supplier.objects.prefetch_related(
        Prefetch(
            'suppliersolution_set',
            queryset=SupplierSolution.objects.select_related('solution').prefetch_related(
                Prefetch(
                    'solution__solutionproblem_set',
                    queryset=SolutionProblem.objects.select_related('problem'),
                    to_attr='problem_links'
                )
            ),
            to_attr='solution_links'
        )
    ).get(id=supplier_id)

    return render(request, 'supplier_detail.html', {
        'supplier': supplier
    })
    
    
def solution_detail(request, solution_id):
    solution = Solution.objects.prefetch_related(
        Prefetch(
            'solutionimpact_set',
            queryset=SolutionImpact.objects.all(),
            to_attr='impact_links'
        )
    ).get(id=solution_id)

    return render(request, 'solution_detail.html', {
        'solution': solution
    })
