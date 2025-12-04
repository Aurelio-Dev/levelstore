
(function() {
  'use strict';

  function getTheme() {
    return localStorage.getItem('theme') || 'dark';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }

 
  function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    updateToggleButton();
  }

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


  document.addEventListener('DOMContentLoaded', function() {
    applyTheme(getTheme());
    updateToggleButton();

   
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }
  });

 
  applyTheme(getTheme());
})();

