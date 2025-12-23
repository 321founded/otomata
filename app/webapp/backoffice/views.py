from django.shortcuts import render, redirect

MOCK_WORKFLOWS = [
    {'id': 1, 'name': 'Enrichissement leads SaaS', 'status': 'active', 'runs': 12, 'last_run': '2024-01-15 14:30'},
    {'id': 2, 'name': 'Veille concurrentielle', 'status': 'active', 'runs': 8, 'last_run': '2024-01-15 09:00'},
    {'id': 3, 'name': 'Onboarding RH automatisé', 'status': 'paused', 'runs': 3, 'last_run': '2024-01-10 11:00'},
    {'id': 4, 'name': 'Rapprochement factures', 'status': 'draft', 'runs': 0, 'last_run': None},
]

MOCK_RUNS = [
    {'id': 1, 'workflow': 'Enrichissement leads SaaS', 'status': 'completed', 'started': '2024-01-15 14:30', 'duration': '2m 34s', 'items': 150},
    {'id': 2, 'workflow': 'Veille concurrentielle', 'status': 'running', 'started': '2024-01-15 15:00', 'duration': '-', 'items': 45},
    {'id': 3, 'workflow': 'Enrichissement leads SaaS', 'status': 'completed', 'started': '2024-01-14 10:00', 'duration': '3m 12s', 'items': 200},
    {'id': 4, 'workflow': 'Onboarding RH automatisé', 'status': 'failed', 'started': '2024-01-10 11:00', 'duration': '0m 45s', 'items': 0},
]

MOCK_DATA = [
    {'id': 1, 'company': 'Acme Corp', 'domain': 'acme.com', 'employees': '50-100', 'industry': 'SaaS', 'score': 85},
    {'id': 2, 'company': 'TechStart', 'domain': 'techstart.io', 'employees': '10-50', 'industry': 'FinTech', 'score': 72},
    {'id': 3, 'company': 'DataFlow', 'domain': 'dataflow.fr', 'employees': '100-250', 'industry': 'Data', 'score': 91},
    {'id': 4, 'company': 'CloudOps', 'domain': 'cloudops.eu', 'employees': '50-100', 'industry': 'DevOps', 'score': 68},
    {'id': 5, 'company': 'GreenTech', 'domain': 'greentech.com', 'employees': '250-500', 'industry': 'CleanTech', 'score': 79},
]


def login(request):
    if request.method == 'POST':
        request.session['logged_in'] = True
        return redirect('backoffice:dashboard')
    return render(request, 'app/login.html')


def logout(request):
    request.session.flush()
    return redirect('backoffice:login')


def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('logged_in'):
            return redirect('backoffice:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_login
def dashboard(request):
    context = {
        'stats': {
            'workflows': len(MOCK_WORKFLOWS),
            'runs_today': 5,
            'items_processed': 1250,
            'success_rate': 94,
        },
        'recent_runs': MOCK_RUNS[:3],
        'workflows': MOCK_WORKFLOWS[:3],
    }
    return render(request, 'app/dashboard.html', context)


@require_login
def workflows_list(request):
    return render(request, 'app/workflows_list.html', {'workflows': MOCK_WORKFLOWS})


@require_login
def workflow_detail(request, pk):
    workflow = next((w for w in MOCK_WORKFLOWS if w['id'] == pk), MOCK_WORKFLOWS[0])
    runs = [r for r in MOCK_RUNS if r['workflow'] == workflow['name']]
    return render(request, 'app/workflow_detail.html', {'workflow': workflow, 'runs': runs})


@require_login
def runs_list(request):
    return render(request, 'app/runs_list.html', {'runs': MOCK_RUNS})


@require_login
def run_detail(request, pk):
    run = next((r for r in MOCK_RUNS if r['id'] == pk), MOCK_RUNS[0])
    logs = [
        {'time': '14:30:01', 'level': 'info', 'message': 'Starting workflow execution'},
        {'time': '14:30:02', 'level': 'info', 'message': 'Fetching data from source API'},
        {'time': '14:30:15', 'level': 'info', 'message': 'Retrieved 150 records'},
        {'time': '14:30:16', 'level': 'info', 'message': 'Starting enrichment process'},
        {'time': '14:32:30', 'level': 'success', 'message': 'Enrichment completed: 145/150 successful'},
        {'time': '14:32:34', 'level': 'info', 'message': 'Workflow completed'},
    ]
    return render(request, 'app/run_detail.html', {'run': run, 'logs': logs})


@require_login
def data(request):
    return render(request, 'app/data.html', {'items': MOCK_DATA})
