from authentication.models import Worker
from request.models import Request


def allot_request_to_worker(request: Request):
    global _worker
    workers_queryset = Worker.objects.filter(worker_type='electrician')
    for worker in workers_queryset:
        if not worker.is_available:
            continue
        _worker = worker
        break
    try:
        request.is_forwarded = True
        request.forwarded_to = _worker  # NameError thrown if it does not exist
    except NameError:
        return False
