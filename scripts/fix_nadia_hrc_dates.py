from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '// Correções específicas: Dra. Nádia (HRC), distinta de Dra. Nádia (EUD) (HRC).'

if marker not in s:
    anchor = 'Object.entries(escala24a31Agosto).forEach(([idTrio,escala])=>aplicarEscalaEspecifica(idTrio,escala));\n\n'
    if anchor not in s:
        raise SystemExit('August schedule anchor not found')

    block = '''// Correções específicas: Dra. Nádia (HRC), distinta de Dra. Nádia (EUD) (HRC).\nfunction corrigirLocalTurnoPatch(idTrio, dataBr, periodo, local) {\n  const infoDia = localizarInfoDiaPatch(String(idTrio), dataBr);\n  if (!infoDia) return;\n  const turno = (infoDia.turnos || []).find(item => item.periodo === periodo);\n  if (turno) turno.local = local;\n}\ncorrigirLocalTurnoPatch(7, "10/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(5, "17/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(4, "24/08", "Manhã", "Dra. Nádia (HRC)");\ncorrigirLocalTurnoPatch(2, "31/08", "Manhã", "Dra. Nádia (HRC)");\n\n'''
    s = s.replace(anchor, anchor + block, 1)

p.write_text(s, encoding='utf-8')
