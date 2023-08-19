from django.shortcuts import render
letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]
# Create your views here.
def index(request):
    array = []
    upper_letters=[]
    for i in range(len(letters)):
        array.append(f'/authors?letter={letters[i]}')
        upper_letters.append(letters[i].upper())
        
    alphabet_pairs = zip(array, upper_letters)    
    return render(request, 'index.html', {'alphabet_pairs': alphabet_pairs})