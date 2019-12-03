from django.shortcuts import render, HttpResponse


def home_view(request):
    if request.user.is_authenticated:
        context = {
            'name': "Berkay",
        }

    else:
        context = {
            'name': 'Guest',
        }
    return render(request, 'home.html', context)



