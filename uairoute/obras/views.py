<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Obra

def cadastrar_obra(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        rua = request.POST.get("rua")
        numero = request.POST.get("numero")
        bairro = request.POST.get("bairro")
        cidade = request.POST.get("cidade")

        Obra.objects.create(
            nome=nome,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade
        )
        return redirect('listar_obras')

    return render(request, "obras/formulario.html")

def listar_obras(request):
    obras = Obra.objects.all().values()
    return JsonResponse(list(obras), safe=False)
=======
from rest_framework import generics
from .models import Obra
from .serializers import ObraSerializer

class ObraListCreateView(generics.ListCreateAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer

class ObraRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
>>>>>>> e7a24774f170565376dea3561ad0ca5ee3829d4c
