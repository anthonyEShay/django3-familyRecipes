from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from json import dumps
from userPages.models import UserProfile

# Create your views here.

def aToZ(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'cookbook/aToZ.html', {'recipes':recipes})

def recipeDetail(request, recipeName):
    recipe = get_object_or_404(Recipe, title=recipeName)
    ingredients = dumps(recipe.ingredients)
    isFavorite = False
    if request.user.is_authenticated:
        userP = UserProfile.objects.get(user=request.user)
        for aRec in userP.favorites.all():
            if aRec.title == recipeName:
                isFavorite = True
                break
    return render(request, 'cookbook/recipeDetail.html', {'recipe':recipe, 'ingList':ingredients, 'isFavorite':isFavorite})

def recipeSearch(request):
    if request.method != 'POST':
        return redirect('home')
    else:
        recipes = Recipe.objects.filter(title__icontains=request.POST['searchText'])
        return render(request, 'cookbook/aToZ.html', {'recipes':recipes})

def shoppingList(request):
    return render(request, 'cookbook/shoppingList.html')

def printableList(request):
    return render(request, 'cookbook/printableList.html')