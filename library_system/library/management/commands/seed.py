from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from library.models import *
import random
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin")
            print("Superuser 'admin' created.")
        
        books_sample = [
            {"title": "A Visit From the Goon Squad", "author": "Jennifer Egan", "published_date": "2010-03-22"},
            {"title": "The Thousand Autumns of Jacob de Zoet", "author": "David Mitchell", "published_date": "2011-03-08"},
            {"title": "Train Dreams", "author": "Denis Johnson", "published_date": "2012-05-22"},
            {"title": "The Buddha in the Attic", "author": "Julie Otsuka", "published_date": "2012-03-20"},
            {"title": "The Tiger's Wife", "author": "Téa Obreht", "published_date": "2011-11-01"},
            {"title": "Salvage the Bones", "author": "Jesmyn Ward", "published_date": "2012-04-24"},
            {"title": "The Flamethrowers", "author": "Rachel Kushner", "published_date": "2014-01-14"},
        ]
        
        for book in books_sample:
            Book.objects.get_or_create(
                title=book["title"],
                author=book["author"],
                published_date=book["published_date"]
            )
                
        all_books = list(Book.objects.all())

        roles = ['admin', 'librarian', 'member']
        for role in roles:
            for i in range(1, 4):
                username = f"{role}{i}"
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, password=username, role=role)
                    rented_books = random.sample(all_books, k=random.randint(0,len(books_sample)))
                    user.rented_books.set(rented_books)


        print("Populated database with sample data")
