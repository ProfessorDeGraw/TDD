from django.shortcuts import redirect, render
from lists.models import Item


# Create your views here.
def home_page(request):
    # TODO(nddegraw) Support more than one list!
    # TODO(nddegraw) Display multiple items in the table
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
