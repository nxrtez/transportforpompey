import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify

# Create your models here.
class Mode(models.Model):
    """
    Bus, Train, Ferry, etc.
    """
    name = models.CharField(
        max_length=20,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = "Mode of transport"
        verbose_name_plural = "Modes of transport"

    def __str__(self):
        return self.name

class VehicleType(models.Model):
    """
    Single-deck bus, double-deck bus, EMU, ferry class, etc.
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Vehicle type"
        verbose_name_plural = "Vehicle types"

    def __str__(self):
        return self.name

class Operator(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    operator_name = models.CharField(
        max_length=50
    )

    bustimes_slug = models.SlugField(
        unique=True,
        help_text="Unique Bustimes.org operator slug"
    )

    website = models.URLField(
        blank=True
    )

    telephone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+44\d{9,12}$',
                message="Telephone must be in +44 format"
            )
        ]
    )

    email = models.EmailField(
        blank=True
    )

    logo_circular = models.ImageField(
        upload_to="operators/logos/circular/",
        blank=True
    )

    logo_banner = models.ImageField(
        upload_to="operators/logos/banner/",
        blank=True,
        help_text="Only used on operator detail pages"
    )

    primary_hex = models.CharField(
        max_length=7,
        help_text="Hex colour, e.g. #0019A8"
    )

    secondary_hex = models.CharField(
        max_length=7,
        blank=True
    )

    vehicles_operated = models.ManyToManyField(
        VehicleType,
        blank=True
    )

    has_custom_page = models.BooleanField(
        default=False,
        help_text="Enable a custom operator page layout"
    )

    custom_template = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional template path, e.g. siteui/operators/stagecoach.html"
    )

    class Meta:
        ordering = ["operator_name"]

    def __str__(self):
        return self.operator_name

class Route(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    service = models.CharField(
        max_length=10,
        help_text="e.g. X4, 1, 2, 3"
    )

    mode = models.ForeignKey(
        Mode,
        on_delete=models.PROTECT,
        related_name="routes"
    )

    operator = models.ForeignKey(
        Operator,
        on_delete=models.PROTECT,
        related_name="routes"
    )

    origin = models.CharField(
        max_length=100
    )

    destination = models.CharField(
        max_length=100
    )

    via = models.CharField(
        max_length=200,
        blank=True
    )

    vehicles_used = models.ManyToManyField(
        VehicleType,
        blank=True,
        related_name="routes"
    )

    route_group = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional grouping label"
    )

    route_hex = models.CharField(
        max_length=7,
        blank=True,
        help_text="Optional route-specific colour (e.g. #0019A8). If empty, operator colour is used."
    )

    bustimes_id = models.IntegerField(
        unique=True,
        help_text="Bustimes.org service ID"
    )

    display_order = models.PositiveIntegerField(
        default=1000,
        help_text="Lower numbers appear first in lists"
    )

    class Meta:
        unique_together = ("service", "operator", "mode")

    def __str__(self):
        return f"{self.service} ({self.operator})"

class Fare(models.Model):
    mode = models.ForeignKey(
        Mode,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Fare"
        verbose_name_plural = "Fares"

    def __str__(self):
        return self.name

class ServiceStatusType(models.Model):
    """
    Official TfL service status terminology and colours.
    Colours must comply with TfL Colour Standard (Issue 10).
    """

    name = models.CharField(
        max_length=30,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    colour_hex = models.CharField(
        max_length=7,
        help_text="TfL-approved hex colour (e.g. #DC241F)"
    )

    class Meta:
        verbose_name = "Service status type"
        verbose_name_plural = "Service status types"
        ordering = ["name"]

    def __str__(self):
        return self.name

class RouteStatus(models.Model):
    """
    Live or scheduled status affecting a route.
    """

    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="statuses"
    )

    status_type = models.ForeignKey(
        ServiceStatusType,
        on_delete=models.PROTECT
    )

    summary = models.CharField(
        max_length=200,
        help_text="Short headline message"
    )

    detail = models.TextField(
        blank=True,
        help_text="Detailed public explanation"
    )

    affected_section = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. 'Between Portsmouth & Fareham'"
    )

    is_planned = models.BooleanField(
        default=False,
        help_text="Planned works or closures"
    )

    is_active = models.BooleanField(
        default=True
    )

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(
        blank=True,
        null=True
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Route status"
        verbose_name_plural = "Route statuses"
        ordering = ["-valid_from"]

    def __str__(self):
        return f"{self.route} – {self.status_type}"

class Ticket(models.Model):
    """
    Operator-specific ticket products.
    """

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=50,
        help_text="e.g. Day Ticket, Weekly Pass"
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Ticket price in GBP"
    )

    duration = models.CharField(
        max_length=50,
        help_text="e.g. Day, Week, Month, Single journey"
    )

    operator = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["operator", "price"]
        unique_together = ("name", "operator")

    def __str__(self):
        return f"{self.name} ({self.operator.operator_name})"

class Map(models.Model):
    """
    Represents a downloadable or viewable transport map.
    """

    title = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    path = models.CharField(
        max_length=255,
        help_text="URL or file path to the map (e.g. /media/maps/bus-network.pdf)"
    )

    preview_image = models.ImageField(
        upload_to="maps/previews/",
        blank=True,
        help_text="Optional PNG preview image"
    )

    hex_colour = models.CharField(
        max_length=7,
        help_text="Hex colour used for bar and outline (e.g. #0019A8)"
    )

    slug = models.SlugField(
        unique=True,
        help_text="Used in map URLs"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Map"
        verbose_name_plural = "Maps"

    def __str__(self):
        return self.title
