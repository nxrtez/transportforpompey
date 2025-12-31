from django.contrib import admin
from .models import (
    Mode,
    Operator,
    VehicleType,
    Route,
    Fare,
    ServiceStatusType,
    RouteStatus,
    Ticket,
    Map,
)

# --------------------
# Core
# --------------------

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "mode",
        "operator",
        "origin",
        "destination",
        "display_order",
    )

    list_editable = ("display_order",)

    list_filter = (
        "mode",
        "operator",
        "route_group",
    )

    search_fields = (
        "service",
        "origin",
        "destination",
    )

    ordering = ("display_order", "service")

    readonly_fields = ("uuid",)

    fieldsets = (
        ("Core", {
            "fields": (
                "uuid",
                "service",
                "mode",
                "operator",
                "display_order",
            )
        }),
        ("Route detail", {
            "fields": (
                "origin",
                "destination",
                "via",
                "route_group",
            )
        }),
        ("Branding", {
            "fields": (
                "route_hex",
            )
        }),
        ("Operations", {
            "fields": (
                "vehicles_used",
            )
        }),
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = (
        "operator_name",
        "bustimes_slug",
        "website",
        "telephone",
        "has_custom_page",
    )

    search_fields = (
        "operator_name",
        "bustimes_slug",
    )

    readonly_fields = ("uuid",)

    fieldsets = (
        ("Identity", {
            "fields": (
                "uuid",
                "operator_name",
                "bustimes_slug",
            )
        }),
        ("Contact", {
            "fields": (
                "website",
                "telephone",
                "email",
            )
        }),
        ("Branding", {
            "fields": (
                "logo_circular",
                "logo_banner",
                "primary_hex",
                "secondary_hex",
            )
        }),
        ("Operations", {
            "fields": (
                "vehicles_operated",
            )
        }),
        ("Custom page", {
            "fields": (
                "has_custom_page",
                "custom_template",
            ),
            "description": (
                "Enable a custom operator page template. "
                "If enabled, the template path must exist."
            ),
        }),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "operator",
        "price",
        "duration",
    )

    list_filter = ("operator",)

    search_fields = (
        "name",
        "operator__operator_name",
    )

    readonly_fields = ("uuid",)

    fieldsets = (
        ("Ticket", {
            "fields": (
                "uuid",
                "name",
                "operator",
            )
        }),
        ("Pricing", {
            "fields": (
                "price",
                "duration",
            )
        }),
        ("Description", {
            "fields": (
                "description",
            )
        }),
    )


@admin.register(Fare)
class FareAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mode",
    )

    list_filter = ("mode",)

    search_fields = ("name",)


# --------------------
# Status
# --------------------

@admin.register(ServiceStatusType)
class ServiceStatusTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(RouteStatus)
class RouteStatusAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "status_type",
        "is_planned",
        "is_active",
        "valid_from",
    )

    list_filter = (
        "status_type",
        "is_planned",
        "is_active",
        "route__mode",
    )

    search_fields = (
        "route__service",
        "summary",
        "affected_section",
    )

    fieldsets = (
        ("Status", {
            "fields": (
                "route",
                "status_type",
                "summary",
                "detail",
            )
        }),
        ("Scope", {
            "fields": (
                "affected_section",
                "is_planned",
            )
        }),
        ("Validity", {
            "fields": (
                "is_active",
                "valid_from",
                "valid_to",
            )
        }),
    )


# --------------------
# Maps
# --------------------

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "path",
        "hex_colour",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    fieldsets = (
        ("Map", {
            "fields": (
                "title",
                "description",
                "slug",
            )
        }),
        ("Preview", {
            "fields": (
                "preview_image",
            )
        }),
        ("Link", {
            "fields": (
                "path",
            )
        }),
        ("Branding", {
            "fields": (
                "hex_colour",
            )
        }),
    )
