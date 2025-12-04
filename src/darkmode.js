// Dark Mode Toggle Script
(function() {
  'use strict';

  // Função para obter o tema atual
  function getTheme() {
    return localStorage.getItem('theme') || 'dark';
  }

  // Função para aplicar o tema
  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }

  // Função para alternar o tema
  function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    updateToggleButton();
  }

  // Função para atualizar o botão de toggle
  function updateToggleButton() {
    const theme = getTheme();
    const toggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');

    if (toggleBtn && sunIcon && moonIcon) {
      if (theme === 'dark') {
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
        toggleBtn.setAttribute('aria-label', 'Mudar para modo claro');
      } else {
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
        toggleBtn.setAttribute('aria-label', 'Mudar para modo escuro');
      }
    }
  }

  // Aplicar tema ao carregar a página
  document.addEventListener('DOMContentLoaded', function() {
    applyTheme(getTheme());
    updateToggleButton();

    // Adicionar event listener ao botão de toggle
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }
  });

  // Aplicar tema imediatamente para evitar flash
  applyTheme(getTheme());
})();
