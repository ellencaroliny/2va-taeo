
import pandas as pd
import numpy as np
from pulp import *

print("=" * 90)
print(" OTIMIZAÇÃO DE CIRURGIAS ONCOLÓGICAS - MÉTODO SIMPLEX (PuLP) ")
print("=" * 90)

procedimentos = {
    'id': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'],
    'procedimento': [
        'Mastectomia (Câncer de Mama)',
        'Prostatectomia (Câncer de Próstata)',
        'Colectomia (Câncer de Cólon)',
        'Gastrectomia (Câncer de Estômago)',
        'Lobectomia (Câncer de Pulmão)',
        'Histerectomia (Câncer de Útero)',
        'Tireoidectomia (Câncer de Tireoide)',
        'Nefrectomia (Câncer de Rim)'
    ],
    'gravidade': [8.5, 7.8, 9.2, 9.5, 9.8, 7.5, 6.5, 8.0],
    'tempo_h': [3.5, 4.0, 5.0, 6.0, 5.5, 3.0, 2.5, 4.5],
    'custo_r': [15000, 18000, 25000, 28000, 35000, 14000, 12000, 22000],
    'uti': [1, 1, 1, 1, 1, 1, 0, 1],
    'incidencia_pe': [3.62, 10.01, 13.71, 7.36, 3.09, 5.20, 4.80, 6.15]
}

df = pd.DataFrame(procedimentos)

print("\n📊 PROCEDIMENTOS ONCOLÓGICOS:")
print(df.to_string(index=False))


def otimizar_cirurgias_pulp(df, orcamento, horas_sala, leitos_uti, criterio='incidencia'):
    """
    Resolve o problema usando PuLP (Simplex com Branch and Bound)
    
    Garante solução ÓTIMA GLOBAL
    """
    
    print(f"\n{'=' * 90}")
    print(f"OTIMIZANDO COM PULP - Critério: {criterio.upper()}")
    print(f"{'=' * 90}")
    

    prob = LpProblem("Cirurgias_Oncologicas", LpMaximize)
    
    # Variáveis de decisão (inteiras)
    n = len(df)
    x = [LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(n)]
    
    # Pesos para função objetivo
    if criterio == 'gravidade':
        w = df['gravidade'].values
    elif criterio == 'incidencia':
        w = df['incidencia_pe'].values
    else:  # custo_beneficio
        w = (df['gravidade'] / df['custo_r'] * 10000).values
    
    # FUNÇÃO OBJETIVO
    prob += lpSum([w[i] * x[i] for i in range(n)]), "Valor_Total"
    
    # RESTRIÇÕES
    # 1. Orçamento
    prob += lpSum([df['custo_r'].iloc[i] * x[i] for i in range(n)]) <= orcamento, "Orcamento"
    
    # 2. Tempo de sala
    prob += lpSum([df['tempo_h'].iloc[i] * x[i] for i in range(n)]) <= horas_sala, "Tempo"
    
    # 3. Leitos UTI
    prob += lpSum([df['uti'].iloc[i] * x[i] for i in range(n)]) <= leitos_uti, "UTI"
    
    # Resolver
    print("⚙️  Executando Simplex...")
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # Verificar status
    status = LpStatus[prob.status]
    print(f"Status: {status}")
    
    if status == 'Optimal':
        # Extrair solução
        solucao = []
        for i in range(n):
            qtd = int(x[i].varValue())
            if qtd > 0:
                solucao.append({
                    'ID': df['id'].iloc[i],
                    'Procedimento': df['procedimento'].iloc[i],
                    'Quantidade': qtd,
                    'Tempo_Total_h': qtd * df['tempo_h'].iloc[i],
                    'Custo_Total_R$': qtd * df['custo_r'].iloc[i],
                    'Leitos_UTI': qtd * df['uti'].iloc[i]
                })
        
        df_sol = pd.DataFrame(solucao)
        
        total_cirurgias = df_sol['Quantidade'].sum()
        total_tempo = df_sol['Tempo_Total_h'].sum()
        total_custo = df_sol['Custo_Total_R$'].sum()
        total_uti = df_sol['Leitos_UTI'].sum()
        valor_obj = value(prob.objective)
        
        print("\n📊 SOLUÇÃO ÓTIMA:")
        print(df_sol.to_string(index=False))
        print(f"\n📈 TOTAIS:")
        print(f"  Cirurgias: {total_cirurgias}")
        print(f"  Tempo: {total_tempo:.1f}h / {horas_sala}h")
        print(f"  Custo: R$ {total_custo:,.2f} / R$ {orcamento:,.2f}")
        print(f"  UTI: {total_uti} / {leitos_uti}")
        print(f"  Valor Objetivo: {valor_obj:.2f}")
        
        return {
            'status': status,
            'solucao': df_sol,
            'metricas': {
                'total_cirurgias': total_cirurgias,
                'total_tempo': total_tempo,
                'total_custo': total_custo,
                'total_uti': total_uti,
                'valor_objetivo': valor_obj
            }
        }
    else:
        print(f"❌ Solução não encontrada: {status}")
        return {'status': status, 'solucao': None, 'metricas': None}
cenarios = {
    'REAL': {
        'orcamento': 500000,
        'horas_sala': 480,
        'leitos_uti': 15,
        'criterio': 'incidencia'
    },
    'OTIMISTA': {
        'orcamento': 800000,
        'horas_sala': 720,
        'leitos_uti': 25,
        'criterio': 'gravidade'
    },
    'PESSIMISTA': {
        'orcamento': 300000,
        'horas_sala': 320,
        'leitos_uti': 8,
        'criterio': 'gravidade'
    }
}


print("\n" + "=" * 90)
print(" RESULTADOS ")
print("=" * 90)

for nome, config in cenarios.items():
    print(f"\n🏥 CENÁRIO {nome}")
    resultado = otimizar_cirurgias_pulp(
        df,
        config['orcamento'],
        config['horas_sala'],
        config['leitos_uti'],
        config['criterio']
    )

print("\n" + "=" * 90)
print("CONCLUSÃO")
print("=" * 90)
print("""
✅ Solução ÓTIMA garantida pelo algoritmo Simplex (via PuLP + CBC)

Este código garante:
1. Solução matematicamente ótima (não heurística)
2. Tempo de execução eficiente (segundos para problemas pequenos/médios)
3. Verificação de viabilidade automática

Para problemas maiores (100+ procedimentos), considerar:
- Heurísticas (Genetic Algorithm, Simulated Annealing)
- Decomposição do problema (Dantzig-Wolfe)
- Programação Estocástica (incerteza nos parâmetros)
""")
