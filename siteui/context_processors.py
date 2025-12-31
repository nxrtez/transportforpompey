from .models import NetworkIncident


def network_incident(request):
    incident = (
        NetworkIncident.objects
        .filter(active=True)
        .select_related("status_type")
        .order_by("-start_time")
        .first()
    )

    return {
        "active_network_incident": incident
    }
