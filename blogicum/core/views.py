from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'core/404.html', status=404)


def csrf_error(request, exception):
    return render(request, 'core/403scrf.html', status=403)


def something_broke(request):
    return render(request, 'core/500.html', status=500)
