from app.database import SessionLocal
from app.models import Profile, Skill, Project

db = SessionLocal()

profile = db.query(Profile).first()
skills = db.query(Skill).all()
projects = db.query(Project).all()

print("Profile:", profile.name)
print("Skills:")
for skill in skills:
    print("-", skill.skill_name)

print("\nProjects:")
for project in projects:
    print("-", project.title)

db.close()