from django.shortcuts import render
from django.db.models import Prefetch
from .models import (
    Mode,
    Route,
    RouteStatus,
    ServiceStatusType,
    Map,
)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Operator, Route, Ticket, Map, RouteStatus


# Create your views here.
def home(request):
    return render(request, "siteui/home.html")

def status_overview(request):
    """
    Single TfL-style status page:
    Mode → Operator → Route
    """

    # Prefetch only ACTIVE statuses, newest first
    active_statuses = RouteStatus.objects.filter(
        is_active=True
    ).select_related(
        "status_type"
    ).order_by(
        "-valid_from"
    )

    routes = Route.objects.select_related(
        "mode",
        "operator",
    ).prefetch_related(
        Prefetch(
            "statuses",
            queryset=active_statuses,
            to_attr="active_statuses"
        )
    ).order_by(
        "service"
    )

    modes = (
        Mode.objects
        .prefetch_related("routes")
        .order_by("name")
    )

    context = {
        "modes": modes,
        "routes": routes,
    }

    return render(request, "siteui/status.html", context)

def maps(request):
    maps = Map.objects.all()
    return render(
        request,
        "siteui/maps.html",
        {
            "maps": maps,
        }
    )

def map_detail(request, slug):
    map_obj = get_object_or_404(Map, slug=slug)
    return redirect(map_obj.path)

def fares(request):
    operators = (
        Operator.objects
        .prefetch_related("tickets")
        .order_by("operator_name")
    )

    return render(
        request,
        "siteui/fares.html",
        {
            "operators": operators,
        }
    )

def operators(request):
    operators = Operator.objects.order_by("operator_name")

    return render(
        request,
        "siteui/operators.html",
        {
            "operators": operators
        }
    )

def stagecoach(request):
    return render(request, "siteui/operators/stagecoach.html")


def first(request):
    return render(request, "siteui/operators/first.html")


def operator_detail(request, slug):
    operator = get_object_or_404(
        Operator,
        bustimes_slug=slug
    )

    routes = (
        Route.objects
        .filter(operator=operator)
        .select_related("mode")
        .order_by("mode__name", "service")
    )

    tickets = (
        Ticket.objects
        .filter(operator=operator)
        .order_by("price")
    )

    # Default template
    template = "siteui/operator_detail.html"

    # Override if custom page enabled
    if operator.has_custom_page and operator.custom_template:
        template = operator.custom_template

    return render(
        request,
        template,
        {
            "operator": operator,
            "routes": routes,
            "tickets": tickets,
        }
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
        }
    )

def route_detail(request, uuid):
    route = get_object_or_404(Route, uuid=uuid)

    # Current active status (if any)
    status = (
        RouteStatus.objects
        .filter(route=route, is_active=True)
        .select_related("status_type")
        .order_by("-valid_from")
        .first()
    )

    # Maps (for now: all maps; later can be filtered by mode/route)
    maps = Map.objects.all()

    # Tickets come from the operator
    tickets = Ticket.objects.filter(operator=route.operator).order_by("price")

    return render(
        request,
        "siteui/route_detail.html",
        {
            "route": route,
            "status": status,
            "maps": maps,
            "tickets": tickets,
        }
    )