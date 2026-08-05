import os

# Os testes não devem herdar o DATABASE_PATH do container: o pytest-django
# cria seu próprio banco temporário a partir do NAME do settings.
os.environ.pop("DATABASE_PATH", None)
