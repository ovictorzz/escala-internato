from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

needle = "return 'Dr. Caio (PNAR) (HRC)';"
flavia_return = "return 'Dra. Flávia (HRC)';"

if needle not in s:
    raise SystemExit('Canonical Caio rule not found')

# Insere a regra de Flávia na mesma função canônica usada pelo filtro, consulta e ranking.
# O teste ignora acento e aceita tanto "Flávia" quanto "Dra. Flávia".
helper_start = s.find('function normalizarAtividadeCanonical(')
helper_end = s.find('return texto;', helper_start)
if helper_start < 0 or helper_end < 0:
    raise SystemExit('Canonical activity helper not found')

helper = s[helper_start:helper_end]
if flavia_return not in helper:
    rule = r"\n      if (/^(?:dra\\.?\\s*)?flavia\\s*\\(hrc\\)$/.test(chave)) return 'Dra. Flávia (HRC)';"
    insert_at = s.find(needle, helper_start, helper_end)
    if insert_at < 0:
        raise SystemExit('Caio rule not found inside canonical helper')
    insert_at += len(needle)
    s = s[:insert_at] + rule + s[insert_at:]

p.write_text(s, encoding='utf-8')
