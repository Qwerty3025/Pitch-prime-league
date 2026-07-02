from django.db import models


# Core is reserved for shared/homepage code. Domain models live in dedicated apps.

class SpecialPoster(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posters/')
    target_url = models.URLField(blank=True, null=True, help_text="Optional link when the poster is clicked")
    is_active = models.BooleanField(default=True, help_text="Whether this poster should be featured on the homepage")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Special Poster"
        verbose_name_plural = "Special Posters"



from django.db import models


class GameRule(models.Model):

    number = models.PositiveIntegerField()

    title = models.CharField(max_length=200)

    rule_description = models.TextField()


    punishment = models.TextField(
        blank=True,
        help_text="Use each point on a new line"
    )


    special_rule = models.TextField(
        blank=True,
        help_text="Use each point on a new line"
    )


    highlight = models.CharField(
        max_length=300,
        blank=True
    )


    def __str__(self):
        return self.title




class EntertainmentFeature(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()


    def __str__(self):
        return self.title




class DisciplineRule(models.Model):

    rule = models.CharField(max_length=300)


    def __str__(self):
        return self.rule


class PartnerLogo(models.Model):
    CATEGORY_CHOICES = [
        ('sponsor', 'Sponsor'),
        ('supplier', 'Supplier'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    logo = models.ImageField(upload_to='partner_logos/')
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name