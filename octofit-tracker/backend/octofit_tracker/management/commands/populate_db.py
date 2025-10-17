
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', first_name='Tony', last_name='Stark'),
            User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password', first_name='Steve', last_name='Rogers'),
            User.objects.create_user(username='batman', email='batman@dc.com', password='password', first_name='Bruce', last_name='Wayne'),
            User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='password', first_name='Diana', last_name='Prince'),
        ]

        # Create activities
        Activity.objects.create(user='ironman', activity_type='Running', duration=30)
        Activity.objects.create(user='captainamerica', activity_type='Cycling', duration=45)
        Activity.objects.create(user='batman', activity_type='Swimming', duration=60)
        Activity.objects.create(user='wonderwoman', activity_type='Yoga', duration=50)

        # Create leaderboard
        Leaderboard.objects.create(user='ironman', points=100)
        Leaderboard.objects.create(user='captainamerica', points=90)
        Leaderboard.objects.create(user='batman', points=95)
        Leaderboard.objects.create(user='wonderwoman', points=98)

        # Create workouts
        Workout.objects.create(name='Full Body', description='A full body workout routine')
        Workout.objects.create(name='Cardio Blast', description='High intensity cardio workout')
        Workout.objects.create(name='Strength Training', description='Build muscle and strength')


        # Create unique index on email for users using pymongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['users'].create_index('email', unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
