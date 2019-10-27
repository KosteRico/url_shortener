from django.db import models

base_url = "https://kosteri.co/"


class LinkModel(models.Model):
    real_url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "\"{}\": {}".format(self.name, self.real_url)
