from django.shortcuts import render, redirect
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
    obras = Obra.objects.all()
    return render(request, "obras/listagem.html", {"obras": obras})
