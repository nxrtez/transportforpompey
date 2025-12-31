from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Map,
    Mode,
    NetworkIncident,
    Operator,
    Route,
    RouteStatus,
    Ticket,
)

FEATURED_OPERATORS = ["Stagecoach", "First Bus"]


def home(request):
    return render(request, "siteui/home.html")


def status_overview(request):
    """
    Single TfL-style status page:
    Mode → Operator → Route
    """

    # Only ACTIVE statuses that are NOT "Good service"
    active_statuses = (
        RouteStatus.objects
        .filter(is_active=True)
        .exclude(status_type__name__iexact="Good service")
        .select_related("status_type")
        .order_by("-valid_from")
    )

    routes = (
        Route.objects
        .select_related("mode", "operator")
        .prefetch_related(
            Prefetch(
                "statuses",
                queryset=active_statuses,
                to_attr="active_statuses",
            )
        )
        # Keep only routes that actually HAVE a non-good active status
        .filter(statuses__in=active_statuses)
        .distinct()
        .order_by(
            "mode__name",
            "operator__operator_name",
            "display_order",
            "service",
        )
    )

    modes = (
        Mode.objects
        .prefetch_related(
            Prefetch("routes", queryset=routes)
        )
        .order_by("name")
    )

    return render(
        request,
        "siteui/status.html",
        {
            "modes": modes,
            "routes": routes,
        },
    )


def maps(request):
    return render(
        request,
        "siteui/maps.html",
        {
            "maps": Map.objects.all(),
        },
    )


def map_detail(request, slug):
    map_obj = get_object_or_404(Map, slug=slug)
    return redirect(map_obj.path)


def fares(request):
    operators = Operator.objects.prefetch_related("tickets").order_by("operator_name")
    return render(request, "siteui/fares.html", {"operators": operators})


def operators(request):
    return render(
        request,
        "siteui/operators.html",
        {"operators": Operator.objects.order_by("operator_name")},
    )


def stagecoach(request):
    return render(request, "siteui/operators/stagecoach.html")


def first(request):
    return render(request, "siteui/operators/first.html")


def operator_detail(request, slug):
    operator = get_object_or_404(Operator, bustimes_slug=slug)

    routes = (
        Route.objects
        .filter(operator=operator)
        .select_related("mode")
        .order_by("mode__name", "display_order", "service")
    )

    tickets = Ticket.objects.filter(operator=operator).order_by("price")

    template = (
        operator.custom_template
        if operator.has_custom_page and operator.custom_template
        else "siteui/operator_detail.html"
    )

    return render(
        request,
        template,
        {
            "operator": operator,
            "routes": routes,
            "tickets": tickets,
        },
    )


def routes(request):
    routes = (
        Route.objects
        .select_related("mode", "operator")
        .prefetch_related("vehicles_used")
        .order_by("mode__name", "display_order", "service")
    )

    modes = Mode.objects.all().order_by("name")

    return render(
        request,
        "siteui/routes.html",
        {
            "routes": routes,
            "modes": modes,
        },
    )


def route_detail(request, uuid):
    route = get_object_or_404(Route, uuid=uuid)

    status = (
        RouteStatus.objects
        .filter(route=route, is_active=True)
        .select_related("status_type")
        .order_by("-valid_from")
        .first()
    )

    return render(
        request,
        "siteui/route_detail.html",
        {
            "route": route,
            "status": status,
            "maps": Map.objects.all(),
            "tickets": Ticket.objects.filter(operator=route.operator).order_by("price"),
        },
    )
