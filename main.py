from engine import BlackjackEngine
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

jogo = BlackjackEngine()

while True: # Loop para jogar várias mãos
    limpar_tela()
    print("--- 🎰 TESTE DE ENGINE V2 (VISUAL) 🎰 ---")
    
    estado = jogo.iniciar_jogo()
    
    while estado['status'] == "JOGANDO":
        print("\n" + "="*30)
        
        cartas_dealer = [c['face'] for c in estado['dealer_hand']]
        print(f"🎩 Dealer: {cartas_dealer}")
       
        cartas_player = [c['face'] for c in estado['player_hand']]
        pontos = estado['player_points']
        print(f"👤 Você:   {cartas_player} (Soma: {pontos})")
        print("="*30)

        acao = input("👉 (H)it [Pedir] ou (S)tand [Parar]? ").lower()
        
        if acao == 'h':
            estado = jogo.hit()
            print(f"📦 Puxou uma carta...")
        elif acao == 's':
            estado = jogo.stand()
            print("🛑 Parou.")
        else:
            print("Comando inválido!")

    print("\n" + "*"*30)
    print(f"🏁 {estado['mensagem'].upper()}")
    
    # Mostra as cartas finais dos jogos
    final_dealer = [c['face'] for c in estado['dealer_hand']]
    final_player = [c['face'] for c in estado['player_hand']]
    
    print(f"🎩 Dealer Final: {final_dealer} ({jogo.calcular_pontos(jogo.mao_dealer)})")
    print(f"👤 Sua Mão Final: {final_player} ({jogo.calcular_pontos(jogo.mao_jogador)})")
    print("*"*30)
    
    dnv = input("\nJogar novamente? (Enter para sim, 'n' para não): ")
    if dnv.lower() == 'n':
        break

print("Fim dos testes.")