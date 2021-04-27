from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserComment
from cookbook.models import Recipe

# Create your views here.

def homePage (request):
    recipesOfWeek = ['Pumpkin Cream Pie', 'Easy Breezy Cheesecake', 'Instant Salsa', 'Perfect Scrambled Eggs']
    recipeList = Recipe.objects.filter(title=recipesOfWeek[0])
    for x in range(1, 4):
        tempSe = Recipe.objects.filter(title=recipesOfWeek[x])
        recipeList = recipeList | tempSe
    #print(recipeList)
    return render(request, 'userPages/index.html', {'recipeList':recipeList})

@login_required
def saveToUserCart(request):
    if request.method == 'POST':
        userP = UserProfile.objects.filter(user=request.user)
        tempCart = request.POST['listToSave']
        try:
            userP.update(savedCart = tempCart)
        except IntegrityError:
            print("Error Adding")
        return userPage(request) #render(request, 'userPages/userPage.html', {'userP':userP[0]})
    else:
        return userPage(request) #render(request, 'userPages/index.html')

@login_required
def loadUserCart(request):
    if request.method == 'POST':
        userP = UserProfile.objects.get(user=request.user)
        tempCart = userP.savedCart
        comments = UserComment.objects.filter(user=request.user)
        return render(request, 'userPages/userPage.html', {'userP':userP, 'loadCart':tempCart, 'userC':comments})
    else:
        return render(request, 'userPages/index.html')

@login_required
def deleteUserCart(request):
    if request.method == 'POST':
        userP = UserProfile.objects.filter(user=request.user)
        try:
            userP.update(savedCart = None)
        except IntegrityError:
            print("Error Adding")
        return userPage(request) #render(request, 'userPages/userPage.html', {'userP':userP[0]})
    else:
        return userPage(request) #render(request, 'userPages/index.html')

def signupUser(request):
    if request.method == 'GET':
        return render(request, 'userPages/signupUser.html', {'form':UserCreationForm() })
    else:
        #Create New User
        if request.POST['password1'] == request.POST['password2']:
            try:
                newUser = User.objects.create_user(request.POST['username'], password=request.POST['password1'] )
                newUser.save()
                login(request, newUser)
                userP = UserProfile(user=newUser)
                userP.save()
                return redirect('userPage')
            except IntegrityError:
               return render(request, 'userPages/signupUser.html', {'form':UserCreationForm(), 'error':'A User with that name already exists.' }) 

        else:
            #Tell user passwords didn't match
            return render(request, 'userPages/signupUser.html', {'form':UserCreationForm(), 'error':'Passwords did not match.' })


@login_required
def userPage (request):
    userP = UserProfile.objects.get(user=request.user)
    comments = UserComment.objects.filter(user=request.user).order_by('-created')
    return render(request, 'userPages/userPage.html', {'userP':userP, 'userC':comments} )


@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'userPages/loginUser.html', {'form':AuthenticationForm() })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'userPages/loginUser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('userPage')

@login_required
def updateFavorite(request, recipeName):
    if request.method == 'POST':
        userP = UserProfile.objects.get(user=request.user)
        isFavorite = True
        for aRec in userP.favorites.all():
            if aRec.title == recipeName:
                isFavorite = False
                userP.favorites.remove(aRec)
                break
        if isFavorite:
            aRec = Recipe.objects.get(title=recipeName)
            userP.favorites.add(aRec)
        return redirect('recipeDetail', recipeName)
    else:
        return redirect('home')

@login_required
def createComment(request):
    if request.method == 'POST':
        userP = UserProfile.objects.filter(user=request.user)
        recipeName = request.POST['recipeName']
        postRecipe = Recipe.objects.filter(title=recipeName)
        commentText = request.POST['commentText']
        try:
            newComment = UserComment(user=request.user, recipe=postRecipe[0], commentText=commentText)
            newComment.save()
            return redirect('recipeDetail', recipeName)
        except (IntegrityError, ValueError) as e:
            print("Error Adding a Comment")
            print(e)
        return redirect('home')
    else:
        return redirect('home')

@login_required
def deleteComment(request):
    if request.method == 'POST':
        delComment = get_object_or_404(UserComment, user=request.user, pk=request.POST['deletePK'])
        try:
            #delComment = UserComment.objects.filter(user=request.user, pk=request.POST['deletePK'])
            delComment.delete()
        except (IntegrityError, ValueError) as e:
            print("Error Deleting a Comment")
            print(e)
        return userPage(request)
    else:
        return redirect('home')