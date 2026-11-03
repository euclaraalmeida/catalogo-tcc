# Catálogo de TCCs — RAD / IFPB

Catálogo acadêmico com API Django REST Framework e cliente web independente. A API pública só permite leitura de trabalhos publicados; a API de gestão exige token.

## Integrantes

- Maria Clara — **confirmar nome completo**
- **preencher nome completo da segunda integrante**

> Antes da entrega, substituam os dois campos pelo nome completo de cada integrante e façam commits identificados pelas contas GitHub de ambas.

## Estrutura

- `backend/`: projeto Django, API, migrations e banco SQLite com dados de demonstração.
- `frontend/`: aplicação web independente, em HTML, CSS e JavaScript.

## Como executar

### API Django

No PowerShell, na pasta `backend`:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py preparar_coordenacao
python manage.py runserver
```

O comando `preparar_coordenacao` cria ou atualiza as duas contas de demonstração e imprime os tokens válidos para uso. Rode-o depois das migrations.

### Front-end

Em outro terminal, na pasta `frontend`:

```powershell
python -m http.server 5500
```

Abra <http://127.0.0.1:5500>. O cliente consulta a API em `http://127.0.0.1:8000`; ele não possui cópia local dos trabalhos. Se o Django estiver parado, a tela exibe uma mensagem de erro.

## Contas de demonstração

| Usuário | Senha | Token |
| --- | --- | --- |
| `coordenacao1` | `RadTcc2026!` | `3caf0920e2efbbd9d7cfc7ce206952abada644cf` |
| `coordenacao2` | `RadTcc2026!` | `b21b499b6fc26f92153deb47e65a951d18a2dc71` |

Use o token assim: `Authorization: Token <token>`. O token não deve ser enviado no JSON do trabalho. O campo `cadastrado_por` é preenchido pelo usuário autenticado.

## Endpoints

| Método | Rota | Acesso | Função |
| --- | --- | --- | --- |
| POST | `/api/token/` | aberto | Obtém token com `username` e `password` |
| GET | `/api/v1/publico/` | público | Raiz navegável da API pública |
| GET | `/api/v1/publico/trabalhos/` | público | Lista paginada e publicada; aceita `search`, `ano`, `curso`, `palavra_chave`, `ordering` e `page` |
| GET | `/api/v1/publico/trabalhos/<id>/` | público | Detalhe somente de trabalho publicado |
| GET | `/api/v1/publico/estatisticas/` | público | Agregações por ano, curso e orientador |
| GET, POST, PUT, PATCH, DELETE | `/api/gestao/trabalhos/` e `/api/gestao/trabalhos/<id>/` | token | CRUD de trabalhos |
| GET, POST, PUT, PATCH, DELETE | `/api/gestao/cursos/`, `/orientadores/`, `/autores/`, `/palavras-chave/` (e detalhe por ID) | token | CRUD de cadastros de apoio |
| GET | `/api/schema/` | aberto | Schema OpenAPI |
| GET | `/api/docs/` | aberto | Documentação Swagger navegável |

Exemplos de busca e filtro:

```text
/api/v1/publico/trabalhos/?search=acessibilidade
/api/v1/publico/trabalhos/?ano=2024&curso=1
/api/v1/publico/trabalhos/?palavra_chave=educação&ordering=-ano&page=2
```

Exemplo para obter token:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"coordenacao1","password":"RadTcc2026!"}'
```

## Decisões para a porta pública

1. **Dados expostos:** somente trabalhos em situação `Publicado`. A lista contém título, ano, curso, orientador e nomes dos autores. O detalhe também fornece resumo, data de defesa, link do PDF, coorientador e palavras-chave. Nota, e-mails e responsável pelo cadastro ficam fora porque não são necessários à consulta pública. ID de trabalho não publicado retorna 404.
2. **Versionamento:** a porta pública usa `/api/v1/publico/`; a porta interna usa `/api/gestao/`, sem versão. Clientes externos podem depender da promessa pública por tempo indeterminado, então mudanças incompatíveis exigem nova versão. O cliente interno é controlado pela coordenação e pode ser atualizado junto com a API.
3. **Limite:** clientes anônimos têm 20 requisições por minuto por IP. Ao exceder o limite, a API responde `429 Too Many Requests` em JSON e inclui `Retry-After`. O contador usa o cache local do Django e reinicia com o processo de desenvolvimento.

## Organização e validações

- `TrabalhoPublicoViewSet` usa `ReadOnlyModelViewSet` e router para lista e detalhe públicos.
- Estatísticas usam `@api_view(['GET'])`, pois são agregações e não um CRUD de entidade.
- Os recursos de gestão usam `ModelViewSet` e routers. A autenticação é por token e as operações exigem usuário autenticado.
- Serializers públicos e de gestão são classes separadas. A porta pública recorta os campos e o queryset; a porta de gestão recebe os dados editáveis.
- Ano futuro, publicação sem nota ou data de defesa, quantidade de autores fora de 1–2 e título repetido no mesmo curso e ano geram erros de validação em JSON.
- Estatísticas são calculadas com agregações do banco e não armazenadas em campos.
- `select_related` e `prefetch_related` reduzem consultas no catálogo.

## Dados de demonstração

O banco SQLite incluído contém 4 cursos, 8 orientadores, 32 autores, 15 palavras-chave e 30 trabalhos de 2021 a 2026. Há trabalhos publicados, defendidos e em andamento, incluindo trabalhos com dois autores. Os dados são fictícios e os links de PDF são ilustrativos.

## Entrega

O repositório deve ser público e submetido no Google Sala de Aula. Antes de enviar, preencham os nomes completos acima, confirmem os tokens no banco que será entregue e façam commits atribuídos aos dois integrantes.
