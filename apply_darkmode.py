#!/usr/bin/env python3
"""
Script para aplicar dark mode nas páginas HTML do projeto Chronix.
Aplica as mudanças necessárias para suportar modo claro/escuro.
"""

import re
from pathlib import Path

# Páginas a serem atualizadas (excluindo index.html e categoria.html que já foram atualizadas)
PAGES_TO_UPDATE = [
    'produto.html',
    'carrinho.html',
    'checkout.html',
    'login.html',
    'ordemRealizada.html'
]

# Botão de toggle HTML
TOGGLE_BUTTON = '''                <button
                  onclick="toggleDarkMode()"
                  class="dark-mode-toggle hover:text-sky-400 transition p-2"
                  aria-label="Toggle dark mode"
                >
                  <svg class="w-5 h-5 hidden dark:block" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path>
                  </svg>
                  <svg class="w-5 h-5 block dark:hidden" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                  </svg>
                </button>'''

def update_html_file(filepath):
    """Atualiza um arquivo HTML com suporte a dark mode."""
    print(f"Atualizando {filepath.name}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Adicionar configuração do Tailwind e script darkmode.js no head
    if 'darkmode.js' not in content:
        cdn_pattern = r'(<script src="https://cdn\.tailwindcss\.com"></script>)'
        replacement = r'''\1
    <script>
      tailwind.config = {
        darkMode: 'class'
      }
    </script>
    <script src="darkmode.js"></script>'''
        content = re.sub(cdn_pattern, replacement, content)

    # 2. Atualizar body tag
    content = re.sub(
        r'<body class="bg-slate-900 text-slate-100">',
        '<body class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 transition-colors duration-200">',
        content
    )

    # 3. Atualizar header
    content = re.sub(
        r'class="(.*?)bg-slate-800/95(.*?)border-slate-700(.*?)"',
        r'class="\1bg-white/95 dark:bg-slate-800/95\2border-slate-200 dark:border-slate-700\3"',
        content
    )

    # 4. Atualizar classes comuns de background
    replacements = [
        # Backgrounds
        (r'\bbg-slate-900\b(?! dark:)', 'bg-white dark:bg-slate-900'),
        (r'\bbg-slate-800\b(?! dark:)', 'bg-slate-100 dark:bg-slate-800'),
        (r'\bbg-slate-700\b(?! dark:)', 'bg-slate-200 dark:bg-slate-700'),
        (r'\bbg-slate-600\b(?! dark:)', 'bg-slate-300 dark:bg-slate-600'),

        # Text colors
        (r'\btext-slate-100\b(?! dark:)', 'text-slate-800 dark:text-slate-100'),
        (r'\btext-slate-200\b(?! dark:)', 'text-slate-700 dark:text-slate-200'),
        (r'\btext-slate-300\b(?! dark:)', 'text-slate-600 dark:text-slate-300'),
        (r'\btext-slate-400\b(?! dark:)', 'text-slate-600 dark:text-slate-400'),

        # Borders
        (r'\bborder-slate-700\b(?! dark:)', 'border-slate-300 dark:border-slate-700'),
        (r'\bborder-slate-600\b(?! dark:)', 'border-slate-300 dark:border-slate-600'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    # 5. Adicionar botão de toggle no navigation (se houver nav com ul)
    if 'toggleDarkMode' not in content and '<nav>' in content and '<ul' in content:
        # Procurar por <ul> dentro de <nav>
        nav_pattern = r'(<nav>.*?<ul[^>]*>)(.*?)(</ul>)'
        match = re.search(nav_pattern, content, re.DOTALL)
        if match:
            ul_start = match.group(1)
            ul_content = match.group(2)
            ul_end = match.group(3)

            # Adicionar <li> com botão de toggle no início da lista
            new_ul_content = f'''
              <li>
{TOGGLE_BUTTON}
              </li>{ul_content}'''

            content = content.replace(match.group(0), ul_start + new_ul_content + ul_end)

    # Salvar se houve mudanças
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filepath.name} atualizado com sucesso!")
    else:
        print(f"  {filepath.name} já estava atualizado ou não precisou de mudanças.")

def main():
    """Função principal."""
    src_dir = Path(__file__).parent / 'src'

    print("Aplicando dark mode nas páginas HTML...")
    print("=" * 50)

    for page_name in PAGES_TO_UPDATE:
        filepath = src_dir / page_name
        if filepath.exists():
            try:
                update_html_file(filepath)
            except Exception as e:
                print(f"✗ Erro ao atualizar {page_name}: {e}")
        else:
            print(f"✗ Arquivo não encontrado: {page_name}")

    print("=" * 50)
    print("Concluído!")
    print("\nLembre-se de:")
    print("1. Revisar as páginas para ajustes finos")
    print("2. Compilar o CSS: npm run dev")
    print("3. Testar o dark mode em cada página")

if __name__ == '__main__':
    main()
