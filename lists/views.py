from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    our_list = List.objects.get(id=list_id)

    return render(
        request,
        "list.html",
        {"list": our_list})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f"/lists/{list_.id}/")


def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")
