from django.test import TestCase
from .models import Skill, Recommendation

class SkillTestCase(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Python", description="A powerful programming language")
        self.recommendation = Recommendation.objects.create(skill=self.skill, description="Recommended for web development")

    def test_skill_name(self):
        self.assertEqual(self.skill.name, "Python")

    def test_recommendation_description(self):
        self.assertEqual(self.recommendation.description, "Recommended for web development")
