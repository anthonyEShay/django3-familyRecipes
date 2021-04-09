"""familyRecipes2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from userPages import views as userViews
from cookbook import views as cookViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # User pages
    path('', userViews.homePage, name = 'home'),
    path('logout/', userViews.logoutUser, name='logoutUser'),
    path('login/', userViews.loginUser, name='loginUser'),
    path('userPage/', userViews.userPage, name='userPage'),
    path('signup/', userViews.signupUser, name='signupUser'),
    path('updateFavorite/<str:recipeName>/', userViews.updateFavorite, name='updateFav'),
    path('saveToUserCart/', userViews.saveToUserCart, name='saveToUserCart'),
    path('deleteUserCart/', userViews.deleteUserCart, name='deleteUserCart'),
    path('loadUserCart/', userViews.loadUserCart, name='loadUserCart'),


    # Cook Book pages
    path('aToZ/', cookViews.aToZ, name = 'aToZ'),
    path('cookbook/<str:recipeName>/', cookViews.recipeDetail, name='recipeDetail'),
    path('cookbook/recipeSearch', cookViews.recipeSearch, name='recipeSearch'),
    path('shoppingList/', cookViews.shoppingList, name='shoppingList'),
    path('printable/', cookViews.printableList, name='printableList'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)