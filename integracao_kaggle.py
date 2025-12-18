"""
Script de Integração com Onco-360 (Kaggle)
Demonstra como carregar dados reais e aplicar otimização

REQUISITOS:
1. pip install kagglehub pandas numpy pulp
2. Configurar Kaggle API (opcional)
   - Criar conta no Kaggle
   - Baixar kaggle.json de https://www.kaggle.com/settings
   - Colocar em ~/.kaggle/kaggle.json
"""

import pandas as pd
import numpy as np
from pulp import *

print("=" * 90)
print(" INTEGRAÇÃO COM DADOS REAIS DO ONCO-360 ")
print("=" * 90)

print("\n📥 Baixando dataset Onco-360...")

try:
    import kagglehub
    path = kagglehub.dataset_download("rafatrindade/onco-360")
    print(f"✅ Download concluído: {path}")
except ImportError:
    print("❌ kagglehub não instalado. Execute: pip install kagglehub")
    path = None
except Exception as e:
    print(f"❌ Erro no download: {e}")
    path = None

if path:
    print("\n📊 Carregando dados do Painel de Oncologia...")
    
    try:
        # Carregar base principal
        df_painel = pd.read_parquet(f"{path}/raw_painel_de_oncologia.parquet")
        
        print(f"✅ Dados carregados: {len(df_painel):,} registros")
        print(f"\n🔍 Colunas disponíveis:")
        print(df_painel.columns.tolist())
        
        print(f"\n📈 Primeiras linhas:")
        print(df_painel.head())
        
        # Análise exploratória
        print(f"\n🔬 ANÁLISE EXPLORATÓRIA")
        print(f"=" * 90)
        
        colunas_interesse = [
            'procedimento', 'tipo_cirurgia', 'tempo_medio', 'custo',
            'complexidade', 'gravidade', 'uf', 'estabelecimento'
        ]
        
        colunas_encontradas = [col for col in colunas_interesse 
                               if col in df_painel.columns]
        
        print(f"\nColunas de interesse encontradas: {colunas_encontradas}")
        
        # Filtrar dados de Pernambuco
        if 'uf' in df_painel.columns or 'UF' in df_painel.columns:
            col_uf = 'uf' if 'uf' in df_painel.columns else 'UF'
            df_pe = df_painel[df_painel[col_uf].isin(['PE', 26])]
            print(f"\n📍 Registros de Pernambuco: {len(df_pe):,}")
        else:
            df_pe = df_painel
            print("\n⚠️  Coluna UF não encontrada, usando dados gerais")
        
        
        print(f"\n🔧 Preparando dados para otimização...")
        

    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
