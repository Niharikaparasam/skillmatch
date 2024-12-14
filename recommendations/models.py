from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.skill.name}"
