"""
populate_db.py - Script to create test data for Octofit Tracker Django backend.

Usage:
    python manage.py shell < populate_db.py

This script creates test users, activities, teams, and leaderboard entries for development/testing.
"""

from django.contrib.auth import get_user_model
from octofit_tracker.models import Activity, Team, Leaderboard
from django.utils import timezone

User = get_user_model()

def create_users():
    users = []
    for i in range(1, 6):
        user, created = User.objects.get_or_create(
            username=f"testuser{i}",
            defaults={
                "email": f"testuser{i}@example.com",
                "is_active": True,
            },
        )
        users.append(user)
    return users

def create_teams(users):
    team1, _ = Team.objects.get_or_create(name="Team Alpha")
    team2, _ = Team.objects.get_or_create(name="Team Beta")
    team1.members.set(users[:3])
    team2.members.set(users[3:])
    return [team1, team2]

def create_activities(users):
    activities = []
    for user in users:
        for j in range(3):
            activity = Activity.objects.create(
                user=user,
                type="Running",
                duration=30 + j * 5,
                distance=5 + j * 2,
                date=timezone.now() - timezone.timedelta(days=j),
            )
            activities.append(activity)
    return activities

def create_leaderboard(teams):
    for team in teams:
        Leaderboard.objects.get_or_create(
            team=team,
            defaults={"points": 100 * team.members.count()},
        )

def main():
    users = create_users()
    teams = create_teams(users)
    create_activities(users)
    create_leaderboard(teams)
    print("Test data created successfully.")

if __name__ == "__main__":
    main()
