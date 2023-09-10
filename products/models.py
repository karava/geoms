from django.db import models


# Choices
UNITS_OF_MEASURE = [
    ('rolls', 'Rolls'),
    ('sqm', 'SQM'),
]

INCOTERMS = [
    ('fob', 'FOB'),
    ('cif', 'CIF'),
    ('ddp', 'DDP'),
]

CURRENCIES = [
    ('usd', 'USD'),
    ('aud', 'AUD'),
]

PRICE_TYPES = [
    ('sale', 'Sale'),
    ('cost', 'Cost'),
    ('rrp', 'RRP'),
]

GEOTEXTILE_TYPES = [
    ('woven', 'Woven'),
    ('nonwoven', 'Non-woven'),
]

GEOGRID_TYPES = [
    ('BI', 'BIAXIAL'),
    ('TRI', 'TRIAXIAL'),
]

DRAINAGE_TYPES = [
    ('strip', 'Strip Drain'),
    ('sheet', 'Sheet Drain'),
]

RESOURCE_TYPES = [
    ('datasheet', 'Datasheet'),
    ('brochure', 'Brochure'),
    ('installation_guide', 'Installation Guide'),
    ('accessory_guide', 'Accessory Guide'),
    ('test_report', 'Test Report'),
]


class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class BaseProduct(models.Model):
    code = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)
    material = models.CharField(max_length=200, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True,
                                         help_text="This is a short concise and useful description of the product")
    long_description = models.TextField(null=True, blank=True, help_text="This is for SEO purposes")
    notes = models.TextField(null=True, blank=True)
    suppliers = models.CharField(max_length=200, null=True, blank=True, help_text="Please comma separate names")
    unit_of_measure = models.CharField(max_length=200, choices=UNITS_OF_MEASURE, default="rolls")
    twentygp_cap = models.IntegerField(null=True, blank=True, default=0)
    fortygp_cap = models.IntegerField(null=True, blank=True, default=0)
    fortyhc_cap = models.IntegerField(null=True, blank=True, default=0)
    moq = models.IntegerField(null=True, blank=True, default=0)
    alternative_names = models.CharField(max_length=200, null=True, blank=True, help_text="Please comma separate names")
    packing_description = models.CharField(max_length=200, null=True, blank=True)
    sub_categories = models.JSONField()

    class Meta:
        abstract = True


class Drainage(BaseProduct):
    type = models.CharField(choices=DRAINAGE_TYPES, max_length=200, default="strip",
                            help_text="FreDrain = Strip Drain, TerraDrain = Sheet Drain")
    height = models.IntegerField(help_text="Unit of measure is mm")
    roll_width = models.IntegerField(help_text="Unit of measure is mm")
    double_cuspated = models.BooleanField(default=False)
    applications = models.ManyToManyField(Application, related_name="drainage_products")

    def __str__(self):
        return "Type: {}, Height: {}x{}".format(self.type, self.height, self.roll_width)


class GCL(BaseProduct):
    density = models.IntegerField(help_text="Unit of measure is gsm")
    roll_width = models.DecimalField(max_digits=4, decimal_places=2, help_text="Unit of measure is m")
    roll_length = models.DecimalField(max_digits=5, decimal_places=2, help_text="Unit of measure is m")
    bentonite_specs = models.CharField(max_length=200, null=True, blank=True)
    applications = models.ManyToManyField(Application, related_name="gcl_products")

    def __str__(self):
        return "Code: {}, Density: {}, Roll Width: {}".format(self.code, self.density, self.roll_width)


class GeoCell(BaseProduct):
    height = models.IntegerField(help_text="Unit of measure is mm")
    weld_spacing = models.IntegerField(help_text="Unit of measure is mm")
    is_textured = models.BooleanField(default=False)
    applications = models.ManyToManyField(Application, related_name="geo_cell_products")

    def __str__(self):
        return "Height: {}, Weld spacing: {}".format(self.height, self.weld_spacing)


class GeoGrid(BaseProduct):
    shape = models.CharField(choices=GEOGRID_TYPES, max_length=200)
    strength_md = models.IntegerField(help_text="Strength in machine direction in kN")
    strength_td = models.IntegerField(help_text="Strength in transverse direction in kN")
    applications = models.ManyToManyField(Application, related_name="geo_grid_products")

    def __str__(self):
        return "Shape: {}, Strength: {}x{}".format(self.shape, self.strength_md, self.strength_td)


class GeoTextile(BaseProduct):
    density = models.IntegerField(help_text="Unit of measure is gsm")
    roll_width = models.DecimalField(max_digits=4, decimal_places=2, help_text="Unit of measure is m")
    roll_length = models.DecimalField(max_digits=5, decimal_places=2, help_text="Unit of measure is m")
    type = models.CharField(choices=GEOTEXTILE_TYPES, max_length=200, default="woven")
    applications = models.ManyToManyField(Application, related_name="geo_textile_products")
    # FIXME: aperture_size do we need this?

    def __str__(self):
        return "Density: {}, Type: {}".format(self.density, self.type)


class BasePrice(models.Model):
    type = models.CharField(max_length=200, choices=PRICE_TYPES, default='sale')
    date = models.DateField()
    qty = models.IntegerField()
    unit_of_measure = models.CharField(max_length=200, choices=UNITS_OF_MEASURE, default="rolls")
    incoterm = models.CharField(max_length=200, choices=INCOTERMS, default="cif")
    location = models.CharField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=200, choices=CURRENCIES, default='usd')
    expiry = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        abstract = True


class DrainagePrice(BasePrice):
    product = models.ForeignKey("Drainage", on_delete=models.CASCADE, related_name="prices")

    def __str__(self):
        return "Title: {}, Code: {}, Type: {}". format(self.product.title, self.product.code, self.type)


class GCLPrice(BasePrice):
    product = models.ForeignKey("GCL", on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return "Title: {}, Code: {}, Type: {}".format(self.product.title, self.product.code, self.type)


class GeoCellPrice(BasePrice):
    product = models.ForeignKey("GeoCell", on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return "Title: {}, Code: {}, Type: {}".format(self.product.title, self.product.code, self.type)


class GeoGridPrice(BasePrice):
    product = models.ForeignKey("GeoGrid", on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return "Title: {}, Code: {}, Type: {}".format(self.product.title, self.product.code, self.type)


class GeoTextilePrice(BasePrice):
    product = models.ForeignKey("GeoTextile", on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return "Title: {}, Code: {}, Type: {}".format(self.product.title, self.product.code, self.type)


class BaseProductImage(models.Model):
    is_default = models.BooleanField(default=True)  # TODO: set all others as False, but do it in views or services

    class Meta:
        abstract = True


class DrainageImage(BaseProductImage):
    image = models.ImageField(upload_to="products/drainage/images/", max_length=255)
    product = models.ForeignKey("Drainage", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return "{}: {}".format(self.product.title, self.pk)


class GCLImage(BaseProductImage):
    image = models.ImageField(upload_to="products/gcl/images/", max_length=255)
    product = models.ForeignKey("GCL", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return "{}: {}".format(self.product.title, self.pk)


class GeoCellImage(BaseProductImage):
    image = models.ImageField(upload_to="products/geo_cell/images/", max_length=255)
    product = models.ForeignKey("GeoCell", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return "{}: {}".format(self.product.title, self.pk)


class GeoGridImage(BaseProductImage):
    image = models.ImageField(upload_to="products/geo_grid/images/", max_length=255)
    product = models.ForeignKey("GeoGrid", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return "{}: {}".format(self.product.title, self.pk)


class GeoTextileImage(BaseProductImage):
    image = models.ImageField(upload_to="products/geo_textile/images/", max_length=255)
    product = models.ForeignKey("GeoTextile", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return "{}: {}".format(self.product.title, self.pk)


class BaseResource(models.Model):
    type = models.CharField(choices=RESOURCE_TYPES, max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class DrainageResource(BaseResource):
    attachment = models.FileField(upload_to="products/drainage/resources/", max_length=255)
    product = models.ForeignKey("Drainage", on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return f"{self.type} for {self.product.code}"


class GCLResource(BaseResource):
    attachment = models.FileField(upload_to="products/gcl/resources/", max_length=255)
    product = models.ForeignKey("GCL", on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return f"{self.type} for {self.product.code}"


class GeoCellResource(BaseResource):
    attachment = models.FileField(upload_to="products/geo_cell/resources/", max_length=255)
    product = models.ForeignKey("GeoCell", on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return f"{self.type} for {self.product.code}"


class GeoGridResource(BaseResource):
    attachment = models.FileField(upload_to="products/geo_grid/resources/", max_length=255)
    product = models.ForeignKey("GeoGrid", on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return f"{self.type} for {self.product.code}"


class GeoTextileResource(BaseResource):
    attachment = models.FileField(upload_to="products/geo_textile/resources/", max_length=255)
    product = models.ForeignKey("GeoTextile", on_delete=models.CASCADE, related_name="resources")

    def __str__(self):
        return f"{self.type} for {self.product.code}"
