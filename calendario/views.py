from django.shortcuts import render
from django.http import JsonResponse 
from .models import Evento

def tela_inicial(request):
    all_events = Evento.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'tela_inicial.html', context)

def all_events(request):                                                                                                 
    all_events = Evento.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.nome,                                                                                         
            'id': event.id,                                                                                              
            'start': event.inicio.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.fim.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Evento(nome=str(title), inicio=start, fim=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Evento.objects.get(id=id)
    event.inicio = start
    event.fim = end
    event.nome = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Evento.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)