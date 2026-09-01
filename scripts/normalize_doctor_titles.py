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
        raise SystemExit('Document write anchor not found for activity normalization')

    caio_block = r'''    // Unifica Caio e Dr. Caio no filtro, consulta e ranking de atividades.
    // Exibe sempre Dr. Caio (PNAR) (HRC) e soma as ocorrências dos dois rótulos.
    const helperAtividadeCanonica = `function normalizarAtividadeCanonical(valor = '') {
      const texto = String(valor || '').replace(/\\s+/g, ' ').trim();
      const chave = texto.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
      if (/^(?:dr\\.?\\s*)?caio\\s*\\(pnar\\)\\s*\\(hrc\\)$/.test(chave)) return 'Dr. Caio (PNAR) (HRC)';
      if (/^(?:dra\\.?\\s*)?flavia\\s*\\(hrc\\)$/.test(chave)) return 'Dra. Flávia (HRC)';
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

# Atualiza instalações existentes da função canônica para também unificar Flávia/Dra. Flávia.
old_rule = r"      if (/^(?:dr\\.?\\s*)?caio\\s*\\(pnar\\)\\s*\\(hrc\\)$/.test(chave)) return 'Dr. Caio (PNAR) (HRC)';\n      return texto;"
new_rule = r"      if (/^(?:dr\\.?\\s*)?caio\\s*\\(pnar\\)\\s*\\(hrc\\)$/.test(chave)) return 'Dr. Caio (PNAR) (HRC)';\n      if (/^(?:dra\\.?\\s*)?flavia\\s*\\(hrc\\)$/.test(chave)) return 'Dra. Flávia (HRC)';\n      return texto;"
if old_rule in s:
    s = s.replace(old_rule, new_rule)

# Dra. Nádia (HRC) é uma preceptora diferente de Dra. Nádia (EUD) (HRC).
# Corrige somente as quatro ocorrências informadas, sem unificar os dois locais.
nadia_marker = '// Correções específicas: Dra. Nádia (HRC), distinta de Dra. Nádia (EUD) (HRC).'
if nadia_marker not in s:
    anchor_nadia = 'Object.entries(escala24a31Agosto).forEach(([idTrio,escala])=>aplicarEscalaEspecifica(idTrio,escala));\n\n'
    if anchor_nadia not in s:
        raise SystemExit('August schedule anchor not found for Nádia corrections')
    nadia_block = '''// Correções específicas: Dra. Nádia (HRC), distinta de Dra. Nádia (EUD) (HRC).\nfunction corrigirLocalTurnoPatch(idTrio, dataBr, periodo, local) {\n  const infoDia = localizarInfoDiaPatch(String(idTrio), dataBr);\n  if (!infoDia) return;\n  const turno = (infoDia.turnos || []).find(item => item.periodo === periodo);\n  if (turno) turno.local = local;\n}\ncorrigirLocalTurnoPatch(7, "10/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(5, "17/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(4, "24/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(2, "31/08", "Manhã", "Dra. Nádia (HRC)");\n\n'''
    s = s.replace(anchor_nadia, anchor_nadia + nadia_block, 1)

p.write_text(s, encoding='utf-8')
