const html = document.documentElement;
const botao = document.getElementById('btnTema');

function aplicarTema(tema) {
    html.setAttribute('data-bs-theme', tema);
    localStorage.setItem('tema', tema);
    botao.textContent = tema === 'dark' ? '☀️ Claro' : '🌙 Escuro';
}

botao.addEventListener('click', () => {
    const atual = html.getAttribute('data-bs-theme');
    aplicarTema(atual === 'dark' ? 'light' : 'dark');
});

// ajusta o texto do botão para o tema que já foi aplicado no <head>
botao.textContent = html.getAttribute('data-bs-theme') === 'dark' ? '☀️ Claro' : '🌙 Escuro';