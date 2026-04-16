from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from user_routes import user_router

app.include_router(auth_router)
app.include_router(user_router)

#para rodar o servidor digitar no terminal: uvicorn main:app --reload

# Uvicorn é a biblioteca responsável por fazer o servidor ir ao ar

#endpoint:  
#/ordens
#é o resto do caminho após o domínio do site.


#REST API's
# Get --> Leitura/Pegar informação
# Post --> Enviar/Criar informação
# put/patch --> Editar informação
# Delete --> Deletar informação
