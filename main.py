import random 

def criar_baralho(numeros_de_decks=1):
    naipes = ['♠️', '♥️', '♦️', '♣️']
    valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    baralho = []

    #loop de decks, no BJ são 6. então ele roda quanto pedirem
    for _ in range(numeros_de_decks):
        
        for naipe in naipes:
            for valor in valores:
                carta = {
                    'face': f"{valor}{naipe}", 
                    'valor_real': valor,
                    'naipe': naipe
                }
                baralho.append(carta)
            
    return baralho

def embaralhar(baralho):
    random.shuffle(baralho)
    return baralho

def dar_carta(baralho):
    # checa as cartas no monte
    if len(baralho) > 0:
        # tira a carta do monte e dá ao player.
        carta = baralho.pop()
        return carta
    else:
        print("Fim de baralho. Trocando o Shoe.")
        return None
    
def calcular_pontos(mao):
    pontos = 0
    ases = 0
    
    for carta in mao:
        valor = carta['valor_real']
        
        if valor in ['J', 'Q', 'K']:
            pontos += 10
        elif valor == 'A':
            ases += 1
            pontos += 11
        else:
            pontos += int(valor)
            
    while pontos > 21 and ases > 0:
        pontos -= 10
        ases -= 1
        
    return pontos

# ... (Mantenha as funções criar_baralho, embaralhar, dar_carta, calcular_pontos iguais) ...

# --- SIMULAÇÃO DE CASSINO (COM DINHEIRO) ---

saldo = 1000 # Bankroll inicial
deck_mesa = criar_baralho(6)
embaralhar(deck_mesa)

print("\n🎰 BEM-VINDO AO FLUXE BET - BLACKJACK 🎰")

while saldo > 0:
    print(f"\n💰 Seu Saldo: C$ {saldo}")
    
    # 1. APOSTA
    try:
        aposta_txt = input("Quanto quer apostar? (Mínimo C$ 50 ou 'q' para sair): ")
        if aposta_txt.lower() == 'q':
            break
        aposta = int(aposta_txt)
    except ValueError:
        print("Digite um número válido!")
        continue

    # VALIDAÇÃO DA APOSTA
    if aposta < 50:
        print("❌ Aposta mínima é C$ 50!")
        continue
    if aposta > saldo:
        print("❌ Saldo insuficiente!")
        continue
    
    saldo -= aposta 
    print(f"Aposta de C$ {aposta} aceita. Boa sorte!")

    # 2. DISTRIBUIÇÃO
    # Se o deck estiver acabando (menos de 20 cartas), cria novo
    if len(deck_mesa) < 20:
        print("embaralhando novo shoe...")
        deck_mesa = criar_baralho(6)
        embaralhar(deck_mesa)

    mao_jogador = [dar_carta(deck_mesa), dar_carta(deck_mesa)]
    mao_dealer = [dar_carta(deck_mesa), dar_carta(deck_mesa)]

    print(f"\nSua mão: {mao_jogador[0]['face']} e {mao_jogador[1]['face']} ({calcular_pontos(mao_jogador)})")
    print(f"Dealer: {mao_dealer[0]['face']} e <Oculta>")

    # 3. CHECAGEM DE BLACKJACK / SEGURO
    pts_jogador = calcular_pontos(mao_jogador)
    pts_dealer = calcular_pontos(mao_dealer)
    
    # (Simplificando: Se alguém tiver BJ na saída, resolve logo)
    if pts_dealer == 21:
        print(f"Dealer revela: {mao_dealer[1]['face']} (Blackjack!)")
        if pts_jogador == 21:
            print("🤝 EMPATE (PUSH). Aposta devolvida.")
            saldo += aposta
        else:
            print("💸 Dealer tem Blackjack. Você perdeu.")
        continue # Vai para a próxima mão

    if pts_jogador == 21:
        print("🌟 BLACKJACK! Você ganhou!")
        # Paga 3:2 (1.5x)
        lucro = aposta * 2.5 
        saldo += int(lucro)
        print(f"Ganhou C$ {lucro}")
        continue

    # 4. TURNO DO JOGADOR
    estourou = False
    while True:
        acao = input(" (H)it [Pedir] ou (S)tand [Parar]? ").lower()
        if acao == 'h':
            nova = dar_carta(deck_mesa)
            mao_jogador.append(nova)
            pts_jogador = calcular_pontos(mao_jogador)
            print(f"📦 {nova['face']} -> Total: {pts_jogador}")
            
            if pts_jogador > 21:
                print("💥 ESTOUROU!")
                estourou = True
                break
        elif acao == 's':
            break
    
    if estourou:
        print("💸 A banca recolhe sua aposta.")
        continue 

    # 5. TURNO DO DEALER
    print(f"\nDealer revela: {mao_dealer[1]['face']}") # Revela a carta oculta

    while True:
        pts_dealer = calcular_pontos(mao_dealer)
        
        # Mostra a mão atual do Dealer bonitinha
        cartas_dealer_txt = " ".join([c['face'] for c in mao_dealer])
        print(f"Dealer tem {pts_dealer} ({cartas_dealer_txt})")
        
        if pts_dealer > 21:
            print("💥 DEALER ESTOUROU! Você ganhou!")
            saldo += aposta * 2
            break
        elif pts_dealer >= 17:
            # Comparações Finais
            if pts_jogador > pts_dealer:
                print(f"🏆 VOCÊ GANHOU! ({pts_jogador} vs {pts_dealer})")
                saldo += aposta * 2
            elif pts_jogador < pts_dealer:
                print(f"💸 A banca ganha. ({pts_dealer} vs {pts_jogador})")
            else:
                print(f"🤝 EMPATE. Aposta devolvida. ({pts_dealer} vs {pts_jogador})")
                saldo += aposta
            break
        else:
            # MUDANÇA AQUI: Agora mostramos qual carta ele puxou
            nova_carta_dealer = dar_carta(deck_mesa)
            mao_dealer.append(nova_carta_dealer)
            print(f"📦 Dealer puxou: {nova_carta_dealer['face']}")
            # O loop roda de novo e recalcula os pontos
            
print("\nFim de jogo! Você saiu com C$ ", saldo)