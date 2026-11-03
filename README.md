# Catálogo de TCCs — primeira metade

Integrante informado: Maria Clara.

Implementados 10 dos 20 requisitos funcionais: RF1 a RF8, RF13 e RF15. Esta etapa contém apenas o projeto Django e a API pública de leitura.

## Executar

No PowerShell, dentro de `backend`:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

O ambiente local já está instalado. Para recriar:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## Endpoints

| Método | Endereço | Resultado |
| --- | --- | --- |
| GET | `/api/v1/publico/` | Raiz da API navegável |
| GET | `/api/v1/publico/trabalhos/` | Lista paginada de publicados |
| GET | `/api/v1/publico/trabalhos/<id>/` | Detalhe de um publicado |
| GET | `/api/v1/publico/estatisticas/` | Quantidades por ano, curso e cinco orientadores com mais publicados |

Exemplos no PowerShell:

```powershell
curl.exe "http://127.0.0.1:8000/api/v1/publico/trabalhos/"
curl.exe "http://127.0.0.1:8000/api/v1/publico/trabalhos/?search=acessibilidade"
curl.exe "http://127.0.0.1:8000/api/v1/publico/trabalhos/?ano=2021&curso=1"
curl.exe "http://127.0.0.1:8000/api/v1/publico/trabalhos/?palavra_chave=Acessibilidade&ordering=-ano&page=1"
curl.exe "http://127.0.0.1:8000/api/v1/publico/estatisticas/"
```

`search` pesquisa título, resumo, nome de autor e nome de orientador. `ano`, `curso` (ID) e `palavra_chave` (termo exato, sem diferenciar maiúsculas) podem ser combinados entre si e com `search`. `ordering` aceita `ano`, `-ano`, `titulo` e `-titulo`. Cada página tem cinco itens; a resposta contém `count`, `next`, `previous` e `results`.

## As três decisões da API pública

1. **Registros e campos:** somente trabalhos com situação Publicado. A lista mostra ID, título, ano, nome e sigla do curso, nome do orientador e nomes dos autores. O detalhe acrescenta resumo, data de defesa, link do PDF, nome do coorientador e palavras-chave. Nota, e-mails, responsável pelo cadastro e trabalhos sem autorização de publicação não fazem parte da resposta. Um trabalho não publicado retorna 404 também pelo ID.
2. **Versionamento:** a porta pública usa `/api/v1/publico/`. Campos dessa versão não serão removidos ou renomeados; uma alteração incompatível terá outra versão, mantendo a v1 disponível. A futura porta interna será `/api/gestao/`, sem versão no endereço, pois seu cliente será controlado pela coordenação e poderá ser atualizado em conjunto. A porta interna ainda não foi implementada.
3. **Limite:** 20 requisições por minuto por IP, compartilhadas entre os endpoints públicos, usando `AnonRateThrottle` como nos slides. A chamada excedente recebe 429, mensagem em JSON e cabeçalho `Retry-After`. O cache local do Django controla a janela; reiniciar o processo limpa esse contador de desenvolvimento.

## Organização

`TrabalhoPublicoViewSet` usa `ReadOnlyModelViewSet` com `DefaultRouter` para lista e detalhe do recurso, sem oferecer escrita. O serializer de detalhe acrescenta campos ao serializer público de lista. A futura escrita terá seu próprio serializer.

As estatísticas usam `@api_view(['GET'])`, pois representam uma consulta agregada, não um CRUD. Os totais são calculados pelo banco com `Count`. Relacionamentos da listagem são carregados com `select_related` e `prefetch_related`.

Foram usados os recursos apresentados nos slides da aula 8: `ModelSerializer`, relacionamentos de leitura, ViewSet, router, `AllowAny`, `SearchFilter`, `OrderingFilter`, `PageNumberPagination`, `AnonRateThrottle` e `django-filter`. Não há templates próprios, formulários Django ou comentários no código.

## Banco desta etapa

O `backend/db.sqlite3` acompanha a atividade com quatro cursos, oito orientadores, 32 autores, 15 palavras-chave e 30 trabalhos distribuídos entre 2021 e 2026. Há 24 publicados, três defendidos e três em andamento. Dois trabalhos têm dois autores, e as palavras-chave são reutilizadas. Nomes e dados são fictícios; os links de PDF em `example.com` são ilustrativos.

Duas contas identificam quem cadastrou os trabalhos: `coordenacao1` e `coordenacao2`. Tokens e acesso à porta fechada ficam para a segunda metade.

## O que falta para os outros 50%

| Requisito | Pendente |
| --- | --- |
| RF9 | Autenticação por token |
| RF10 | CRUD de trabalhos pela coordenação |
| RF11 | CRUD dos cadastros de apoio |
| RF12 | Validações de ano, publicação, autores e unicidade |
| RF14 | Schema OpenAPI e documentação navegável |
| RF16 | Front-end separado e configuração de CORS |
| RF17 | Listagem no front-end |
| RF18 | Busca e filtro no front-end |
| RF19 | Detalhe no front-end |
| RF20 | Estados de vazio e erro no front-end |

A tecnologia do front-end, o segundo integrante e as credenciais com tokens serão registrados quando essa parte for realizada. Não há repositório Git inicializado nem envio ao GitHub nesta etapa.
