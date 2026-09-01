from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Mantém a correção do loader que evita a tela preta.
old_decl = '    const directFaceIdMenuFix = `<script id="direct-faceid-menu-fix-v2">'
new_decl = '    const directFaceIdMenuFixV2 = `<script id="direct-faceid-menu-fix-v2">'
if old_decl in s:
    before, after = s.split(old_decl, 1)
    after = after.replace("html=html.replace('</body>',directFaceIdMenuFix+'</body>');", "html=html.replace('</body>',directFaceIdMenuFixV2+'</body>');", 1)
    s = before + new_decl + after

s = s.replace('#boot{display:none;', '#boot{display:grid;', 1)
s = s.replace('<div id="boot"><div class="boot-card"></div></div>', '<div id="boot"><div class="boot-card">Carregando Painel T7A…</div></div>', 1)

# Escala recebida em 31/08/2026 — período de 01/09 a 06/09.
marker = '// Escala recebida em 31/08/2026 — período de 01/09 a 06/09.'
if marker not in s:
    anchor = '''Object.entries(escala24a31Agosto).forEach(([idTrio,escala])=>aplicarEscalaEspecifica(idTrio,escala));

// Atividades noturnas gerais adicionais, aplicadas após todas as escalas individuais.'''
    if anchor not in s:
        raise SystemExit('Schedule insertion anchor not found')

    patch = r'''Object.entries(escala24a31Agosto).forEach(([idTrio,escala])=>aplicarEscalaEspecifica(idTrio,escala));

// Escala recebida em 31/08/2026 — período de 01/09 a 06/09.
// Mantém compromissos acadêmicos fixos e os dias explicitamente marcados como mantém/continua.
const datasAssistenciais01a06Setembro = ["01/09","02/09","03/09","04/09","05/09","06/09"];
const manterDiasSetembro = {
  "4": new Set(["01/09","02/09"]),
  "5": new Set(["03/09","04/09","05/09","06/09"]),
  "6": new Set(["02/09","03/09","04/09","05/09"])
};
const normalizarPatchSetembro = (valor) => String(valor || "").normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
const compromissoAcademicoFixoSetembro = (turno) => {
  const texto = normalizarPatchSetembro(turno?.local);
  return texto.includes("seminario")
    || texto.includes("simulado")
    || texto.includes("sessoes clinicas integradas")
    || texto.includes("sci")
    || texto.includes("aula teorica")
    || texto.includes("avaliacao somativa")
    || texto.includes("somativa");
};
const horarioBasePorPeriodoSetembro = {"Manhã":"07h-13h","Tarde":"13h-18h","Noite":"18h-22h"};

// Nos dias informados, turnos não enviados ficam livres, exceto compromissos acadêmicos fixos.
for (let i=1;i<=10;i++) {
  const idTrio=String(i);
  datasAssistenciais01a06Setembro.forEach(data=>{
    if (manterDiasSetembro[idTrio]?.has(data)) return;
    const infoDia=localizarInfoDiaPatch(idTrio,data);
    if(!infoDia) return;
    (infoDia.turnos||[]).forEach(turno=>{
      if(compromissoAcademicoFixoSetembro(turno)) return;
      turno.local="—";
      if(horarioBasePorPeriodoSetembro[turno.periodo]) turno.horario=horarioBasePorPeriodoSetembro[turno.periodo];
    });
  });
}

const escala01a06Setembro = {
"1":{"01/09":{manha:"BL (HRC)",tarde:"CO (HRC)"},"02/09":{manha:"Dr. Caio (PNAR) (HRC)"},"03/09":{manha:"BL (HRC)",tarde:"Lucimara (HRC)"},"04/09":{manha:"CC (HRC)"},"06/09":{noite:"CO (HRC)"}},
"2":{"01/09":{manha:"PS FICHA (HRC)",tarde:"Marta (HRC)"},"03/09":{tarde:"CO (HRC)"},"04/09":{manha:"Dr. Metódio (HRC)"},"06/09":{tarde:"CO (HRC)"}},
"3":{"01/09":{tarde:"PS FICHA (HRC)"},"03/09":{manha:"PS BOX (HRC)",tarde:"Hellen (ECO) (HRC)"},"04/09":{manha:"PS BOX (HRC)",tarde:"CO (HRC)"},"06/09":{tarde:"CO (HRC)"}},
"4":{"03/09":{manha:"Poli (Dra. Mirna) (HRC)",tarde:"CC (HRC)"},"04/09":{tarde:"Dra. Flávia (HRC)",noite:"CO (HRC)"}},
"5":{"02/09":{manha:"Poli (Dra. Mirna) (HRC)"}},
"6":{},
"7":{"01/09":{manha:"CO (HRC)"},"02/09":{manha:"Amb UNIEURO"},"03/09":{noite:"CO (HRC)"},"04/09":{manha:"F. Mota (HRC)",tarde:"PS FICHA (HRC)"}},
"8":{"01/09":{manha:"ALCON (HRC)",tarde:"PS BOX (HRC)"},"03/09":{manha:"ALCON (HRC)",tarde:"PS FICHA (HRC)"},"04/09":{manha:"Nádia (EUD) (HRC)"},"05/09":{manha:"PS BOX (HRC)"},"06/09":{manha:"ALCON (HRC)"}},
"9":{"01/09":{manha:"CC (HRC)",tarde:"Sádia (HRC)"},"03/09":{tarde:"Dr. Caio (PNAR) (HRC)",noite:"PS FICHA (HRC)"},"04/09":{manha:"CO (HRC)",tarde:"Poli (Dra. Mirna) (HRC)"},"06/09":{manha:"PS BOX (HRC)"}},
"10":{"01/09":{manha:"ALCON (HRC)"},"02/09":{manha:"Amb UNIEURO"},"03/09":{manha:"ALCON (HRC)",tarde:"Sádia (HRC)"},"04/09":{manha:"Dr. Caio (PNAR) (HRC)"},"06/09":{manha:"ALCON (HRC)"}}
};
Object.entries(escala01a06Setembro).forEach(([idTrio,escala])=>aplicarEscalaEspecifica(idTrio,escala));

// Reaplica horários-base; PS FICHA, PS BOX e Amb UNIEURO recebem os horários especiais depois.
for (let i=1;i<=10;i++) {
  const idTrio=String(i);
  datasAssistenciais01a06Setembro.forEach(data=>{
    if (manterDiasSetembro[idTrio]?.has(data)) return;
    const infoDia=localizarInfoDiaPatch(idTrio,data);
    if(!infoDia) return;
    (infoDia.turnos||[]).forEach(turno=>{
      if(compromissoAcademicoFixoSetembro(turno)) return;
      if(turno.local && turno.local !== "—" && horarioBasePorPeriodoSetembro[turno.periodo]) {
        turno.horario=horarioBasePorPeriodoSetembro[turno.periodo];
      }
    });
  });
}

// A escala assistencial publicada termina em 06/09. Depois disso, preserva apenas atividades acadêmicas fixas.
for (let i=1;i<=10;i++) {
  const idTrio=String(i);
  for (let semana=1;semana<=9;semana++) {
    const dias=dadosEscala[idTrio]?.semanas?.[semana]||{};
    Object.values(dias).forEach(infoDia=>{
      const [dd,mm]=String(infoDia?.data||"").split("/").map(Number);
      const depoisDe06Set = (mm===9 && dd>6) || mm>9;
      if(!depoisDe06Set) return;
      (infoDia.turnos||[]).forEach(turno=>{
        if(compromissoAcademicoFixoSetembro(turno)) return;
        turno.local="—";
        if(horarioBasePorPeriodoSetembro[turno.periodo]) turno.horario=horarioBasePorPeriodoSetembro[turno.periodo];
      });
    });
  }
}

// Atividades noturnas gerais adicionais, aplicadas após todas as escalas individuais.'''
    s = s.replace(anchor, patch, 1)

old_dates = 'const datasEscalaRecebida24a31=["24/08","25/08","26/08","27/08","28/08","29/08","30/08","31/08"];'
new_dates = 'const datasEscalaRecebida24a31=["24/08","25/08","26/08","27/08","28/08","29/08","30/08","31/08","01/09","02/09","03/09","04/09","05/09","06/09"];'
if old_dates in s:
    s = s.replace(old_dates, new_dates, 1)
elif new_dates not in s:
    raise SystemExit('Dates confirmation anchor not found')

# Padroniza títulos médicos nas escalas já injetadas. As aspas deixam a substituição idempotente.
name_fixes = {
    '"Caio (PNAR) (HRC)"': '"Dr. Caio (PNAR) (HRC)"',
    '"Metódio (HRC)"': '"Dr. Metódio (HRC)"',
    '"Flávia (HRC)"': '"Dra. Flávia (HRC)"',
}
for old_name, new_name in name_fixes.items():
    s = s.replace(old_name, new_name)

# Validação estrutural antes de salvar: impede reintroduzir a tela preta.
if s.count('const directFaceIdMenuFix =') != 1:
    raise SystemExit('Loader validation failed: duplicate directFaceIdMenuFix')
if 'const directFaceIdMenuFixV2 =' not in s:
    raise SystemExit('Loader validation failed: V2 declaration missing')
if marker not in s:
    raise SystemExit('September schedule marker missing')
for required_name in ['Dr. Caio (PNAR) (HRC)', 'Dr. Metódio (HRC)', 'Dra. Flávia (HRC)']:
    if required_name not in s:
        raise SystemExit(f'Doctor title correction missing: {required_name}')

p.write_text(s, encoding='utf-8')
