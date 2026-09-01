from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '// Padronização global de títulos médicos no conteúdo carregado.'
if marker not in s:
    anchor = '    document.open();\n'
    if anchor not in s:
        raise SystemExit('Document write anchor not found')

    block = '''    // Padronização global de títulos médicos no conteúdo carregado.\n    // Isso evita duplicidades no filtro quando a mesma pessoa aparece com e sem Dr./Dra.\n    const rotulosMedicosPadronizados = [\n      ['\"Adnir (ECO) (HRC)\"', '\"Dra. Adnir (ECO) (HRC)\"'],\n      ['\"Caio (PNAR) (HRC)\"', '\"Dr. Caio (PNAR) (HRC)\"'],\n      ['\"Metódio (HRC)\"', '\"Dr. Metódio (HRC)\"'],\n      ['\"Flávia (HRC)\"', '\"Dra. Flávia (HRC)\"'],\n      ['\"F. Mota (HRC)\"', '\"Dr. F. Mota (HRC)\"'],\n      ['\"Gilmária (HRC)\"', '\"Dra. Gilmária (HRC)\"'],\n      ['\"Hellen (ECO) (HRC)\"', '\"Dra. Hellen (ECO) (HRC)\"'],\n      ['\"Lorena (ECO) (HRC)\"', '\"Dra. Lorena (ECO) (HRC)\"'],\n      ['\"Lucimara (HRC)\"', '\"Dra. Lucimara (HRC)\"'],\n      ['\"Marta (HRC)\"', '\"Dra. Marta (HRC)\"'],\n      ['\"Nádia (EUD) (HRC)\"', '\"Dra. Nádia (EUD) (HRC)\"'],\n      ['\"Rocha (HRC)\"', '\"Dr. Rocha (HRC)\"'],\n      ['\"Sádia (HRC)\"', '\"Dra. Sádia (HRC)\"']\n    ];\n    for (const [semTitulo, comTitulo] of rotulosMedicosPadronizados) {\n      html = html.split(semTitulo).join(comTitulo);\n    }\n\n'''
    s = s.replace(anchor, block + anchor, 1)

caio_marker = '// Unifica Caio e Dr. Caio no filtro, consulta e ranking de atividades.'
if caio_marker not in s:
    anchor = '    document.open();\n'
    if anchor not in s:
        raise SystemExit('Document write anchor not found for Caio normalization')

    caio_block = r'''    // Unifica Caio e Dr. Caio no filtro, consulta e ranking de atividades.
    // Exibe sempre Dr. Caio (PNAR) (HRC) e soma as ocorrências dos dois rótulos.
    const helperAtividadeCanonica = `function normalizarAtividadeCanonical(valor = '') {
      const texto = String(valor || '').replace(/\\s+/g, ' ').trim();
      const chave = texto.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
      if (/^(?:dr\\.?\\s*)?caio\\s*\\(pnar\\)\\s*\\(hrc\\)$/.test(chave)) return 'Dr. Caio (PNAR) (HRC)';
      return texto;
    }\n\n`;
    if (html.includes('function obterAtividadesDisponiveis() {') && !html.includes('function normalizarAtividadeCanonical(')) {
      html = html.replace('function obterAtividadesDisponiveis() {', helperAtividadeCanonica + 'function obterAtividadesDisponiveis() {');
    }
    html = html.split('if (atividadeVisivelNoFiltro(turno.local)) atividades.add(turno.local);')
      .join('if (atividadeVisivelNoFiltro(turno.local)) atividades.add(normalizarAtividadeCanonical(turno.local));');
    html = html.split('if (turno.local !== atividade) return;')
      .join('if (normalizarAtividadeCanonical(turno.local) !== normalizarAtividadeCanonical(atividade)) return;');

'''
    s = s.replace(anchor, caio_block + anchor, 1)

p.write_text(s, encoding='utf-8')
