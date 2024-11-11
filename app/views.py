from django.shortcuts import render, redirect
from sqlalchemy import create_engine, Table, Column, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse

# Set up SQLAlchemy connection
engine = create_engine('sqlite:///profile.db')
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# Define the user table
users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('credits', Integer)
)

# Ensure the table exists
metadata.create_all(engine)

def main(request):
    return render(request, 'main.html')

def add_credit(request):
    user_id = request.GET.get('user_id')
    if user_id:
        with engine.connect() as conn:
            user = conn.execute(users_table.select().where(users_table.c.user_id == user_id)).first()
            if user:
                new_credits = user.credits + 100
                conn.execute(users_table.update().where(users_table.c.user_id == user_id).values(credits=new_credits))
                return JsonResponse({'status': 'success', 'new_credits': new_credits})
            else:
                return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User ID not provided'})
