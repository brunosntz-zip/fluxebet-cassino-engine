# 🎰 FLUXE BET - Blackjack Engine (CLI)

Engine de Cassino desenvolvida em Python focado na lógica matemática do Blackjack (21).
Este projeto simula um ambiente real de cassino, incluindo gestão de banca (eWallet), regras de Dealer e múltiplos baralhos reais.

## 🧠 Lógica Implementada

- **Shoe Profissional:** Simulação de 6 baralhos misturados (312 cartas).
- **Dealer AI:** Implementação da regra "Dealer para com 17 e compra com 16".
- **Dealer Peek:** O Dealer checa Blackjack antecipadamente se mostrar Ás ou 10 na primeira carta virada.
- **Sistema de Apostas:** Gestão de Saldo (Bankroll), validação de aposta mínima e payouts (1:1 e 3:2).
- **Game Loop:** Tratamento de estados (Vitória, Derrota, Empate/Push, Estouro/Bust).

## 🛠️ Tecnologias
- **Python 3.14**
- **Lógica de Dados:** Listas, Dicionários e Manipulação de Estado.

## 🚀 Como Rodar
1. Clone o repositório.
2. Execute o arquivo principal:
   ```bash
   python main.py
