'use client';
import React, { useState } from 'react';

export default function Home() {
  const [trioId, setTrioId] = useState('1');

  const dadosEscala = {
    '1': [
      { bloco: 'BLOCO 1', local: 'HRC - Centro Obstétrico', datas: '01/08 a 31/08', ativo: true },
      { bloco: 'BLOCO 2', local: 'HRAN - Enfermaria', datas: '01/09 a 30/09', ativo: false },
      { bloco: 'BLOCO 3', local: 'HRSM - Ambulatório', datas: '01/10 a 31/10', ativo: false }
    ],
    '2': [
      { bloco: 'BLOCO 1', local: 'Policlínica Ceilândia', datas: '01/08 a 31/08', ativo: true },
      { bloco: 'BLOCO 2', local: 'HRC - Centro Obstétrico', datas: '01/09 a 30/09', ativo: false },
      { bloco: 'BLOCO 3', local: 'HRAN - Enfermaria', datas: '01/10 a 31/10', ativo: false }
    ],
    '3': [
      { bloco: 'BLOCO 1', local: 'HRAN - Enfermaria', datas: '01/08 a 31/08', ativo: true },
      { bloco: 'BLOCO 2', local: 'HRSM - Ambulatório', datas: '01/09 a 30/09', ativo: false },
      { bloco: 'BLOCO 3', local: 'Policlínica Ceilândia', datas: '01/10 a 31/10', ativo: false }
    ],
    '4': [
      { bloco: 'BLOCO 1', local: 'HRSM - Ambulatório', datas: '01/08 a 31/08', ativo: true },
      { bloco: 'BLOCO 2', local: 'Policlínica Ceilândia', datas: '01/09 a 30/09', ativo: false },
      { bloco: 'BLOCO 3', local: 'HRC - Centro Obstétrico', datas: '01/10 a 31/10', ativo: false }
    ],
    '5': [
      { bloco: 'BLOCO 1', local: 'HRC - Enfermaria', datas: '01/08 a 31/08', ativo: true },
      { bloco: 'BLOCO 2', local: 'HRAN - Centro Obstétrico', datas: '01/09 a 30/09', ativo: false },
      { bloco: 'BLOCO 3', local: 'HRSM - Ambulatório', datas: '01/10 a 31/10', ativo: false }
    ]
  };

  const blocosAtuais = dadosEscala[trioId];
  const cenarioAtual = blocosAtuais.find(b => b.ativo)?.local || 'Não definido';

  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#fafafa', minHeight: '100vh', display: 'flex', justifyContent: 'center', paddingBottom: '40px' }}>
      <div style={{ width: '100%', maxWidth: '400px', backgroundColor: '#ffffff', minHeight: '100vh', padding: '24px', boxSizing: 'border-box' }}>
        
        {/* Header */}
        <div style={{ color: '#4f46e5', fontWeight: 'bold', fontSize: '20px', marginBottom: '24px' }}>
          🩺 Internato Médico G.O.
        </div>

        {/* Seletor de Trio */}
        <div style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '16px', padding: '16px', marginBottom: '20px' }}>
          <div style={{ fontSize: '12px', color: '#64748b', fontWeight: '600', marginBottom: '4px' }}>Grupo Selecionado</div>
          <select 
            value={trioId} 
            onChange={(e) => setTrioId(e.target.value)}
            style={{ width: '100%', background: 'transparent', border: 'none', fontWeight: 'bold', fontSize: '14px', color: '#1e293b', outline: 'none' }}
          >
            <option value="1">Trio 1 - Leticia, Bruno & Marta</option>
            <option value="2">Trio 2 - Lus, Carp & amily</option>
            <option value="3">Trio 3 - Sofia, Camla & Уста</option>
            <option value="4">Trio 4 - Ava, BARBADO & And</option>
            <option value="5">Trio 5 - Carolina, Rayane & Annelut</option>
          </select>
        </div>

        {/* Badges e Progresso */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
          <span style={{ backgroundColor: '#ecfdf5', color: '#047857', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold' }}>⏱️ 336h total</span>
          <span style={{ backgroundColor: '#eef2ff', color: '#4338ca', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold' }}>📈 33% completo</span>
        </div>

        {/* Rodízios */}
        <h3 style={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '12px' }}>📅 Rodízios do Internato</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
          {blocosAtuais.map((item, index) => (
            <div 
              key={index} 
              style={{
                border: item.ativo ? '2px solid #6366f1' : '1px solid #e2e8f0',
                backgroundColor: item.ativo ? '#f5f3ff' : '#ffffff',
                borderRadius: '16px',
                padding: '16px'
              }}
            >
              <div style={{ fontSize: '11px', fontWeight: 'bold', color: item.ativo ? '#4f46e5' : '#94a3b8', textTransform: 'uppercase', marginBottom: '4px' }}>{item.bloco}</div>
              <div style={{ fontWeight: 'bold', color: '#0f172a', marginBottom: '4px' }}>{item.local}</div>
              <div style={{ fontSize: '13px', color: '#64748b' }}>{item.datas}</div>
            </div>
          ))}
        </div>

        {/* Cenário Atual */}
        <div style={{ border: '1px solid #e2e8f0', borderRadius: '16px', padding: '16px', backgroundColor: '#ffffff' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '13px', fontWeight: 'bold', color: '#334155' }}>📍 Cenário Atual</span>
            <span style={{ backgroundColor: '#10b981', color: '#ffffff', fontSize: '10px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px' }}>MAPEADO</span>
          </div>
          <div style={{ fontWeight: '900', fontSize: '16px', color: '#0f172a', textTransform: 'uppercase' }}>{cenarioAtual}</div>
        </div>

      </div>
    </div>
  );
}
