from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=30)
    titles = models.IntegerField(null=True, default=0)
    top_scorer = models.CharField(max_length=50)
    fifa_code = models.CharField(max_length=3, unique=True)
    founded_at = models.DateField(null=True)

    def __repr__(self) -> str:
        return f"<[{self.id}] {self.name} - {self.fifa_code}>"
