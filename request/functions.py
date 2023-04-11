from request.models import Request
from worker.models import Worker


def assign_request_to_worker(request_id, worker_type='electrician'):
    request = Request.objects.get(pk=request_id)
    for worker in Worker.objects.all().order_by('rating'):
        if not worker.is_available:
            continue
        if not worker.worker_type == worker_type:
            continue
        request.forwarded_to = worker
        request.is_forwarded = True
        request.save()
        return True
    if not request.is_forwarded:
        return False
