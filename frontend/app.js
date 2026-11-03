const API = 'http://127.0.0.1:8000/api/v1/publico';
const form = document.querySelector('#filters');
const searchInput = document.querySelector('#search');
const yearSelect = document.querySelector('#year');
const courseSelect = document.querySelector('#course');
const orderingSelect = document.querySelector('#ordering');
const cards = document.querySelector('#cards');
const notice = document.querySelector('#notice');
const count = document.querySelector('#result-count');
const pagination = document.querySelector('#pagination');
const dialog = document.querySelector('#detail-dialog');
let activeUrl = `${API}/trabalhos/`;
let debounce;

function queryUrl() {
  const params = new URLSearchParams();
  const q = searchInput.value.trim();
  if (q) params.set('search', q);
  if (yearSelect.value) params.set('ano', yearSelect.value);
  if (courseSelect.value) params.set('curso', courseSelect.value);
  if (orderingSelect.value) params.set('ordering', orderingSelect.value);
  return `${API}/trabalhos/${params.size ? `?${params}` : ''}`;
}

function setLoading() {
  cards.replaceChildren(); pagination.replaceChildren(); count.textContent = '';
  notice.className = 'notice'; notice.textContent = 'Carregando trabalhos…';
}

async function load(url = queryUrl()) {
  activeUrl = url;
  setLoading();
  try {
    const response = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`A API respondeu com o status ${response.status}.`);
    const data = await response.json();
    render(data);
  } catch (error) {
    notice.className = 'notice error';
    notice.textContent = 'Não foi possível carregar o catálogo. Confira se o servidor da API está ligado e tente novamente.';
    count.textContent = '';
  }
}

function render(data) {
  const items = data.results || [];
  cards.replaceChildren();
  count.textContent = `${data.count} ${data.count === 1 ? 'trabalho' : 'trabalhos'}`;
  if (!items.length) {
    notice.className = 'notice empty';
    notice.textContent = 'Nenhum trabalho encontrado. Tente outro termo ou remova os filtros.';
  } else {
    notice.className = 'notice'; notice.textContent = '';
    items.forEach(item => {
      const card = document.createElement('article');
      card.className = 'card'; card.tabIndex = 0; card.setAttribute('role', 'button');
      card.setAttribute('aria-label', `Ver detalhes de ${item.titulo}`);
      const meta = document.createElement('div'); meta.className = 'card-meta';
      const course = document.createElement('span'); course.className = 'course-tag'; course.textContent = item.curso.sigla || item.curso.nome;
      const year = document.createElement('span'); year.textContent = item.ano;
      meta.append(course, year);
      const title = document.createElement('h3'); title.textContent = item.titulo;
      const bottom = document.createElement('div'); bottom.className = 'card-bottom';
      const authors = document.createElement('span'); authors.textContent = (item.autores || []).join(', ');
      const advisor = document.createElement('span'); advisor.textContent = item.orientador;
      bottom.append(authors, advisor); card.append(meta, title, bottom);
      card.addEventListener('click', () => showDetail(item.id));
      card.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); showDetail(item.id); } });
      cards.append(card);
    });
  }
  renderPagination(data);
}

function renderPagination(data) {
  pagination.replaceChildren();
  if (!data.previous && !data.next) return;
  const prev = document.createElement('button'); prev.textContent = '← Anterior'; prev.disabled = !data.previous;
  prev.addEventListener('click', () => load(data.previous));
  const next = document.createElement('button'); next.textContent = 'Próxima →'; next.disabled = !data.next;
  next.addEventListener('click', () => load(data.next));
  pagination.append(prev, document.createTextNode('Resultados paginados'), next);
}

async function loadFilterOptions() {
  try {
    const response = await fetch(`${API}/estatisticas/`, { headers: { Accept: 'application/json' } });
    if (!response.ok) return;
    const stats = await response.json();
    (stats.trabalhos_por_ano || []).forEach(row => yearSelect.add(new Option(row.ano, row.ano)));
    (stats.trabalhos_por_curso || []).forEach(row => courseSelect.add(new Option(`${row.curso__sigla} · ${row.curso__nome}`, row.curso_id)));
  } catch {}
}

async function showDetail(id) {
  const target = document.querySelector('#detail-content');
  target.textContent = 'Carregando…'; dialog.showModal();
  try {
    const response = await fetch(`${API}/trabalhos/${id}/`, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error();
    const item = await response.json(); target.replaceChildren();
    const heading = document.createElement('h2'); heading.id = 'detail-title'; heading.textContent = item.titulo;
    const meta = document.createElement('p'); meta.className = 'detail-meta';
    meta.textContent = `${item.ano} · ${item.curso.nome} (${item.curso.sigla}) · Orientação: ${item.orientador} · Autoria: ${(item.autores || []).join(', ')}`;
    const abstract = document.createElement('p'); abstract.className = 'abstract'; abstract.textContent = item.resumo;
    const labels = document.createElement('div'); labels.className = 'keywords';
    (item.palavras_chave || []).forEach(word => { const tag = document.createElement('span'); tag.textContent = word; labels.append(tag); });
    target.append(heading, meta, abstract, labels);
    if (item.link_pdf) { const link = document.createElement('a'); link.href = item.link_pdf; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Acessar arquivo do trabalho ↗'; target.append(link); }
  } catch { target.textContent = 'Não foi possível carregar os detalhes deste trabalho.'; }
}

form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('change', () => load());
searchInput.addEventListener('input', () => { clearTimeout(debounce); debounce = setTimeout(() => load(), 350); });
document.querySelector('#clear-search').addEventListener('click', () => { searchInput.value = ''; load(); searchInput.focus(); });
searchInput.addEventListener('input', () => { document.querySelector('#clear-search').hidden = !searchInput.value; });
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
loadFilterOptions();
load();
