const inputBusca = document.querySelector('input[name="busca"]');
const sugestoes = document.getElementById('sugestoes');

inputBusca.addEventListener('input', function () {
const query = this.value;

if (query.length < 2) {
    sugestoes.innerHTML = '';
    return;
}

fetch(`/buscar/?bd=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
    sugestoes.innerHTML = '';

    if (data.resultados.length === 0) {
        sugestoes.innerHTML = '<li class="list-group-item">Nenhum resultado</li>';
    } else {/* aqui se usa resultados pois na view foi passado como resultados */
        data.resultados.forEach(produto => {
        const item = document.createElement('li');
        item.classList.add('list-group-item');
        item.innerHTML = 
        `<a href="/produto/${produto.id}" class="text-decoration-none text-dark d-block sugestao">
            <img src="${produto.imagem}" width="80" height="80" class="me-3 rounded">${produto.nome}
        </a>`;
        sugestoes.appendChild(item);
        });
    }
    });
});

// Esconde as sugestões se clicar fora
document.addEventListener('click', function (e) {
if (!inputBusca.contains(e.target) && !sugestoes.contains(e.target)) {
    sugestoes.innerHTML = '';
}
});
