from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

from .models import Funcionario
from .serializers import FuncionarioSerializer


class FuncionarioListCreateView(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    def perform_create(self, serializer):
        senha = serializer.validated_data.get('senha')
        senha_criptografada = make_password(senha)
        serializer.save(senha=senha_criptografada)


class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


class FuncionarioLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        if not email or not senha:
            return Response({"erro": "Email e senha são obrigatórios."}, status=400)

        try:
            funcionario = Funcionario.objects.get(email=email)
            if check_password(senha, funcionario.senha):
                return Response({
                    "mensagem": "Login bem-sucedido",
                    "id": funcionario.id,
                    "nome": funcionario.nome_completo,
                    "is_admin": funcionario.is_admin
                })
            else:
                return Response({"erro": "Senha incorreta"}, status=401)
        except Funcionario.DoesNotExist:
            return Response({"erro": "Usuário não encontrado"}, status=404)
