from django.http import JsonResponse


def health(request):
    """Sonda do healthcheck do Docker.

    Não consulta o banco de propósito: na branch demo cada visitante tem o
    seu, e o healthcheck não tem sessão para escolher um.
    """
    return JsonResponse({"status": "ok"})
