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

p.write_text(s, encoding='utf-8')
