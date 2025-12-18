# 🏥 Otimização de Cirurgias Oncológicas - Método Simplex

Sistema de otimização para agendamento de cirurgias oncológicas na rede pública de Pernambuco, utilizando Programação Linear Inteira e o Método Simplex.

**Autora:** Ellen Caroliny Tavares  
**Instituição:** Universidade Federal Rural de Pernambuco (UFRPE)  
**Disciplina:** Tópicos de Otimização  
**Professor:** Cláudio Cristino

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Problema](#problema)
- [Metodologia](#metodologia)
- [Dados](#dados)
- [Instalação](#instalação)
- [Uso](#uso)
- [Resultados](#resultados)
- [Referências](#referências)

---

## 🎯 Sobre o Projeto

Este projeto aplica técnicas de **Pesquisa Operacional** para otimizar o agendamento de cirurgias oncológicas em hospitais públicos de referência em Pernambuco.
O objetivo é **maximizar o atendimento** de pacientes oncológicos, priorizando casos mais graves, respeitando restrições de:
- ⏱️ **Tempo** disponível em salas cirúrgicas
- 💰 **Orçamento** mensal do hospital
- 🏥 **Leitos de UTI** disponíveis para pós-operatório

---

## 🔬 Problema

### Contexto

A fila de cirurgias oncológicas no SUS é um problema crítico de saúde pública. Pacientes aguardam meses por procedimentos que, em muitos casos, têm urgência devido ao risco de progressão da doença.

A gestão tradicional da fila (FIFO - First In, First Out) não considera:
- **Gravidade clínica** do paciente
- **Disponibilidade de recursos** (salas, equipes, UTI)
- **Custo-efetividade** dos procedimentos

### Formulação Matemática

#### Variáveis de Decisão
```
x_i = número de vezes que o procedimento i será realizado
      (i = 1, 2, ..., n procedimentos)
```

#### Função Objetivo (Maximizar)
```
Z = Σ (w_i × x_i)

onde w_i pode ser:
  - Gravidade clínica (0-10)
  - Incidência populacional (casos/100k hab)
  - Custo-benefício (gravidade/custo)
```

#### Restrições

1. **Orçamento:**
   ```
   Σ (custo_i × x_i) ≤ Orçamento_Mensal
   ```

2. **Tempo de Sala:**
   ```
   Σ (tempo_i × x_i) ≤ Horas_Disponíveis
   ```

3. **Leitos de UTI:**
   ```
   Σ (uti_i × x_i) ≤ Leitos_Disponíveis
   ```

4. **Integralidade:**
   ```
   x_i ∈ {0, 1, 2, 3, ...}  (inteiros não-negativos)
   ```

---

## 🧮 Metodologia

### Algoritmo: Simplex + Branch and Bound

1. **Simplex (George Dantzig, 1947)**
   - Resolve Programação Linear (variáveis contínuas)
   - Percorre vértices do poliedro de soluções viáveis
   - Complexidade: O(n³) no pior caso, mas eficiente na prática

2. **Branch and Bound**
   - Extensão para variáveis inteiras (PLI)
   - Cria árvore de subproblemas
   - Garante solução ótima global

### Implementação

- **Versão Didática:** Heurística gulosa (demonstração)
- **Versão Produção:** PuLP + CBC Solver (solução ótima)

---

## 📊 Dados

### Dataset: Onco-360

Fonte: [Kaggle - Onco-360](https://www.kaggle.com/datasets/rafatrindade/onco-360)

Data Hub desenvolvido para centralizar dados oncológicos do Brasil:
- **DATASUS:** Sistema de Informações Hospitalares (SIH/SUS)
- **INCA:** Instituto Nacional de Câncer
- **CNES:** Cadastro Nacional de Estabelecimentos de Saúde
- **SIOPS:** Sistema de Informações sobre Orçamentos Públicos em Saúde

### Procedimentos Incluídos

| ID | Procedimento | Gravidade | Tempo (h) | Custo (R$) | UTI |
|----|--------------|-----------|-----------|------------|-----|
| P1 | Mastectomia (Câncer de Mama) | 8.5 | 3.5 | 15.000 | Sim |
| P2 | Prostatectomia (Câncer de Próstata) | 7.8 | 4.0 | 18.000 | Sim |
| P3 | Colectomia (Câncer de Cólon) | 9.2 | 5.0 | 25.000 | Sim |
| P4 | Gastrectomia (Câncer de Estômago) | 9.5 | 6.0 | 28.000 | Sim |
| P5 | Lobectomia (Câncer de Pulmão) | 9.8 | 5.5 | 35.000 | Sim |
| P6 | Histerectomia (Câncer de Útero) | 7.5 | 3.0 | 14.000 | Sim |
| P7 | Tireoidectomia (Câncer de Tireoide) | 6.5 | 2.5 | 12.000 | Não |
| P8 | Nefrectomia (Câncer de Rim) | 8.0 | 4.5 | 22.000 | Sim |

*Dados baseados em médias do SIH/SUS para Pernambuco*

---

## 🚀 Instalação

### Requisitos

- Python 3.8+
- pip

### Dependências

```bash
# Versão simplificada (apenas pandas/numpy)
pip install pandas numpy

# Versão completa (com PuLP)
pip install pandas numpy pulp

# Opcional: download automático de dados
pip install kagglehub
```

### Clonar Repositório

```bash
git clone https://github.com/seu-usuario/otimizacao-onco-simplex.git
cd otimizacao-onco-simplex
```

---

## 💻 Uso

### Versão Simplificada (Sem Dependências Externas)

```bash
python otimizacao_onco_simplex.py
```

**Saída:**
- ✅ Solução para 3 cenários (Real, Otimista, Pessimista)
- 📊 Análise comparativa
- 📈 Análise de sensibilidade (variação de orçamento)
- 📚 Exemplo didático completo

### Versão com PuLP (Solução Ótima Garantida)

```bash
python otimizacao_onco_pulp.py
```

**Vantagens:**
- ✅ Solução matematicamente ótima
- ⚡ Rápido (segundos para problemas médios)
- 🔍 Detecção automática de inviabilidade

### Jupyter Notebook (Interativo)

```bash
jupyter notebook otimizacao_analise.ipynb
```

---

## 📈 Resultados

### Cenário Real - PROCAPE/HCP

**Recursos:**
- Orçamento: R$ 500.000/mês
- Horas de Sala: 480h
- Leitos UTI: 15

**Solução Ótima:**
- **25 cirurgias/mês**
- Uso de orçamento: 99,0%
- Uso de tempo: 20,8%
- Uso de UTI: 100,0%

**Composição:**
- 15x Colectomia (Câncer de Cólon)
- 10x Tireoidectomia (Câncer de Tireoide)

### Comparação de Cenários

| Cenário | Cirurgias | Custo (R$) | Tempo (h) | UTI |
|---------|-----------|------------|-----------|-----|
| **Real** | 25 | 495.000 | 100 | 15 |
| **Otimista** | 23 | 798.000 | 127 | 23 |
| **Pessimista** | 9 | 292.000 | 46 | 8 |

**Observação:** Redução de 40% no orçamento resulta em redução de ~64% no número de cirurgias.

### Análise de Sensibilidade

| Variação Orçamento | Cirurgias |
|-------------------|-----------|
| -20% (R$ 400k) | 17 |
| -10% (R$ 450k) | 21 |
| 0% (R$ 500k) | 25 |
| +10% (R$ 550k) | 29 |
| +20% (R$ 600k) | 33 |

**Taxa marginal:** +4 cirurgias por R$ 50mil adicionais

---

## 🎓 Exemplo Didático

### Cenário Fictício

**Local:** Bloco cirúrgico do PROCAPE  
**Recursos:**
- 1 Sala: 6 horas livres
- 1 Leito de UTI vago

**Pacientes:**

1. **Sr. José** - Gastrectomia (Câncer de Estômago Avançado)
   - Risco: ALTÍSSIMO (10/10)
   - Tempo: 6h
   - Necessita UTI: Sim

2. **Dona Ana** - Mastectomia (Câncer de Mama)
   - Risco: ALTO (8/10)
   - Tempo: 3h
   - Necessita UTI: Sim

3. **Sr. Carlos** - Tireoidectomia (Câncer de Tireoide)
   - Risco: MÉDIO (6/10)
   - Tempo: 2h
   - Necessita UTI: Não

### Análise pelo Simplex

**Opção 1:** Ana + Carlos
- ✅ Tempo: 5h (cabe nas 6h)
- ❌ UTI: Precisa de 2 leitos (só tem 1)

**Opção 2:** Apenas Sr. José
- ✅ Tempo: 6h (exato)
- ✅ UTI: 1 leito (exato)
- ✅ Valor: 10 (maior prioridade)

**Solução Ótima:** Operar o Sr. José

**Conclusão:** A restrição de UTI forçou priorização do caso mais grave, mesmo que operando menos pacientes.

---

## 📚 Referências

### Trabalhos Acadêmicos

1. **Pazin-Filho, A. et al. (2024)**  
   *"Surgical waiting lists and queue management in a Brazilian tertiary public hospital"*  
   Demonstra impacto da gestão de filas na mortalidade durante COVID-19

2. **Winston, W. L. (2004)**  
   *"Operations Research: Applications and Algorithms"*  
   Capítulo: Integer Programming

### Bases de Dados

- **Onco-360:** https://www.kaggle.com/datasets/rafatrindade/onco-360
- **DATASUS/SIH:** http://tabnet.datasus.gov.br/
- **INCA:** https://www.inca.gov.br/

### Ferramentas

- **PuLP:** https://coin-or.github.io/pulp/
- **CBC Solver:** https://github.com/coin-or/Cbc

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autora

**Ellen Caroliny Tavares**  
Bacharelado em Sistemas de Informação  
Universidade Federal Rural de Pernambuco (UFRPE)
