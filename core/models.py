from django.db import models


class Setting(models.Model):
    logo = models.ImageField(upload_to="logo", null=True, blank=True)
    site_name = models.CharField(max_length=100, null=True, blank=True)
    site_title = models.CharField(max_length=100, null=True, blank=True)
    site_description = models.TextField(null=True, blank=True)

    background_image = models.ImageField(upload_to="background", null=True, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
