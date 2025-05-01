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

document.addEventListener('DOMContentLoaded', function() {
  const btnAdd = document.querySelector('.add');  // Botão "+"
  const btnSubtract = document.querySelector('.subtract');  // Botão "-"
  const inputQtd = document.querySelector('#qtd');  // Campo de quantidade
  const form = document.querySelector('#form-add-carrinho'); // Formulário

  // Função para aumentar a quantidade
  btnAdd.addEventListener('click', function() {
    let quantidadeAtual = parseInt(inputQtd.value);
    inputQtd.value = quantidadeAtual + 1;  // Incrementa a quantidade
  });

  // Função para diminuir a quantidade
  btnSubtract.addEventListener('click', function() {
    let quantidadeAtual = parseInt(inputQtd.value);
    if (quantidadeAtual > 1) {  // Impede de ir para um número negativo
      inputQtd.value = quantidadeAtual - 1;  // Decrementa a quantidade
    }
  });

  // Evento de submit para garantir que a quantidade seja atualizada corretamente
  form.addEventListener('submit', function(event) {
    let quantidadeAtual = parseInt(inputQtd.value);
    
    // Impede envio do formulário caso a quantidade não seja válida
    if (quantidadeAtual < 1) {
      event.preventDefault();  // Cancela o envio do formulário
      alert('A quantidade precisa ser no mínimo 1.');
      return;
    }

    // Aqui você pode garantir que o valor correto da quantidade será enviado
    inputQtd.value = quantidadeAtual;
  });
});
