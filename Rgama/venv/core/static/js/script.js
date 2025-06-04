document.addEventListener('DOMContentLoaded', function () {

  /* ========== BUSCA DINÂMICA ========== */
  const inputBusca = document.querySelector('input[name="busca"]');
  const sugestoes = document.getElementById('sugestoes');

  if (inputBusca && sugestoes) {
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
          } else {
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

    document.addEventListener('click', function (e) {
      if (!inputBusca.contains(e.target) && !sugestoes.contains(e.target)) {
        sugestoes.innerHTML = '';
      }
    });
  }

  /* ========== CONTROLE DE QUANTIDADE + PARCELAMENTO ========== */
  const btnAdd = document.querySelector('.add');
  const btnSubtract = document.querySelector('.subtract');
  const inputQtd = document.querySelector('#qtd');
  const form = document.querySelector('#form-add-carrinho');
  const valorParcelado = document.querySelector('#parcelado');

  const precoElement = document.getElementById('preco-unidade');
  const precoUnitario = precoElement ? parseFloat(precoElement.dataset.valor) : 0;

  function atualizarParcelamento() {
    if (!valorParcelado || isNaN(precoUnitario)) return;

    const qtd = parseInt(inputQtd.value) || 1;
    const total = precoUnitario * qtd;
    const totalcomjuros = total * 1.10;
    const parcela = (totalcomjuros / 10).toFixed(2).replace('.', ','); // corrigido pra 10x
    valorParcelado.innerText = `Ou 10x R$ ${parcela} no cartão`;
  }

  if (btnAdd && btnSubtract && inputQtd) {
    btnAdd.addEventListener('click', () => {
      inputQtd.value = parseInt(inputQtd.value) + 1;
      atualizarParcelamento();
    });

    btnSubtract.addEventListener('click', () => {
      const atual = parseInt(inputQtd.value);
      if (atual > 1) {
        inputQtd.value = atual - 1;
        atualizarParcelamento();
      }
    });

    inputQtd.addEventListener('input', () => {
      if (parseInt(inputQtd.value) < 1 || isNaN(inputQtd.value)) {
        inputQtd.value = 1;
      }
      atualizarParcelamento();
    });
  }

  if (form && inputQtd) {
    form.addEventListener('submit', function (event) {
      const quantidadeAtual = parseInt(inputQtd.value);
      if (quantidadeAtual < 1) {
        event.preventDefault();
        alert('A quantidade precisa ser no mínimo 1.');
      }
    });
  }

  atualizarParcelamento(); // Inicializa no carregamento

  /* ========== REMOVER DO CARRINHO ========== */
  window.removerDoCarrinho = function(produtoid) {
    const form = document.getElementById('remover-form');
    if (form) {
      form.action = `/carrinho/rmv/${produtoid}`;
      form.submit();
    }
  };

  /* ========== MÁSCARA DE TELEFONE ========== */
  const telefoneInput = document.getElementById("telefone");
  if (telefoneInput && typeof Inputmask !== 'undefined') {
    Inputmask({"mask": "(99) 99999-9999"}).mask(telefoneInput);
  }

});
