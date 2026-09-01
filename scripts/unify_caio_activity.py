from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '// Unifica Caio e Dr. Caio no filtro/consulta/ranking de atividades.'

if marker not in s:
    anchor = '    document.open();\n'
    if anchor not in s:
        raise SystemExit('Document write anchor not found')

    block = r'''    // Unifica Caio e Dr. Caio no filtro/consulta/ranking de atividades.
    // A lista passa a exibir sempre "Dr. Caio (PNAR) (HRC)" e as ocorrências dos dois rótulos são somadas.
    const activityCanonicalHelper = `function normalizarAtividadeCanonical(valor = '') {
      const texto = String(valor || '').replace(/\\s+/g, ' ').trim();
      const chave = texto.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
      if (/^(?:dr\\.?\\s*)?caio\\s*\\(pnar\\)\\s*\\(hrc\\)$/.test(chave)) return 'Dr. Caio (PNAR) (HRC)';
      return texto;
    }\n\n`;
    if (html.includes('function obterAtividadesDisponiveis() {') && !html.includes('function normalizarAtividadeCanonical(')) {
      html = html.replace('function obterAtividadesDisponiveis() {', activityCanonicalHelper + 'function obterAtividadesDisponiveis() {');
    }
    html = html.split('if (atividadeVisivelNoFiltro(turno.local)) atividades.add(turno.local);')
      .join('if (atividadeVisivelNoFiltro(turno.local)) atividades.add(normalizarAtividadeCanonical(turno.local));');
    html = html.split('if (turno.local !== atividade) return;')
      .join('if (normalizarAtividadeCanonical(turno.local) !== normalizarAtividadeCanonical(atividade)) return;');

'''
    s = s.replace(anchor, block + anchor, 1)

p.write_text(s, encoding='utf-8')
