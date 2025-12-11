import random

class BlackjackEngine:
    def __init__(self):
        self.baralho = []
        self.saldo = 1000 # Começa stack de mil
        self.aposta_atual = 0
        self.mao_jogador = []
        self.mao_dealer = []
        self.status = "APOSTANDO" 
        self.resultado = "" 
        self.mensagem = "Faça sua aposta!"
    
    def criar_baralho(self, num_decks=6):
        naipes = ['♠️', '♥️', '♦️', '♣️']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.baralho = []
        for _ in range(num_decks):
            for naipe in naipes:
                for valor in valores:
                    self.baralho.append({'face': f"{valor}{naipe}", 'valor': valor})
        random.shuffle(self.baralho)

    def dar_carta(self):
        if len(self.baralho) < 10: # Acabando o Shoe ele embaralha td dnv
            self.criar_baralho()
        return self.baralho.pop()

    def calcular_pontos(self, mao):
        pontos = 0
        ases = 0
        for carta in mao:
            val = carta['valor']
            if val in ['J', 'Q', 'K', '10']:
                pontos += 10
            elif val == 'A':
                ases += 1
                pontos += 11
            else:
                pontos += int(val)
        while pontos > 21 and ases > 0:
            pontos -= 10
            ases -= 1
        return pontos

    def apostar(self, valor):
        if valor > self.saldo or valor <= 0:
            self.mensagem = "Saldo insuficiente ou valor inválido!"
            return False
        
        self.aposta_atual = valor
        self.saldo -= valor
        self.iniciar_rodada()
        return True

    def adicionar_saldo(self):
        self.saldo += 1000
        self.mensagem = "Recarga de C$ 1.000 efetuada!"

    def iniciar_rodada(self):
        if not self.baralho: self.criar_baralho()
        
        self.mao_jogador = [self.dar_carta(), self.dar_carta()]
        self.mao_dealer = [self.dar_carta(), self.dar_carta()]
        self.status = "JOGANDO"
        self.resultado = ""
        self.mensagem = "Sua vez! Hit, Stand ou Double?"

        # dealer peek
        dealer_val = self.calcular_pontos(self.mao_dealer)
        carta_aberta_val = self.mao_dealer[0]['valor']
        
        # Se dealer tem, ele ve e se tiver acaba o jogo
        if carta_aberta_val in ['A', '10', 'J', 'Q', 'K']:
            if dealer_val == 21:
                self.finalizar_turno_dealer() # Acaba o jogo agr

    def hit(self):
        self.mao_jogador.append(self.dar_carta())
        if self.calcular_pontos(self.mao_jogador) > 21:
            self.status = "FINALIZADO"
            self.resultado = "DERROTA"
            self.mensagem = "Estourou (Bust)! A casa ganha."
    
    def double(self):
        if self.saldo >= self.aposta_atual:
            self.saldo -= self.aposta_atual # Paga mais uma bet
            self.aposta_atual *= 2 
            self.mao_jogador.append(self.dar_carta()) # Recebe mais uma carta só
            
            if self.calcular_pontos(self.mao_jogador) > 21:
                self.status = "FINALIZADO"
                self.resultado = "DERROTA"
                self.mensagem = "Estourou no Double!"
            else:
                self.stand() # para (stand) sozinho depois do Dobrar
        else:
            self.mensagem = "Saldo insuficiente para Dobrar!"

    def stand(self):
        self.finalizar_turno_dealer()

    def finalizar_turno_dealer(self):
        self.status = "FINALIZADO"
        
        pts_player = self.calcular_pontos(self.mao_jogador)
        pts_dealer_inicial = self.calcular_pontos(self.mao_dealer)

        # 1. TRAVA DE SEGURANÇA: BLACKJACK NATURAL
        # Se o jogador tem 21 com 2 cartas (BJ), ele ganha IMEDIATAMENTE.
        # (A não ser que o dealer também tivesse BJ, mas isso já foi checado no início da rodada/Peek)
        if pts_player == 21 and len(self.mao_jogador) == 2:
            self.resultado = "VITORIA"
            self.saldo += int(self.aposta_atual * 2.5) # Paga 3:2
            self.mensagem = "BLACKJACK! 👑 (Paga 3:2)"
            return # O Dealer nem joga, sai da função aqui mesmo.

        # 2. Se o jogador estourou, o dealer também não precisa jogar (economiza carta)
        if pts_player > 21:
            self.resultado = "DERROTA"
            self.mensagem = "Você estourou (Bust)."
            return

        # 3. Agora sim: Se o jogo tá valendo, o Dealer aplica a regra do 17
        while self.calcular_pontos(self.mao_dealer) < 17:
            self.mao_dealer.append(self.dar_carta())
            
        pts_dealer_final = self.calcular_pontos(self.mao_dealer)
        
        # 4. Comparações Finais
        if pts_dealer_final > 21:
            self.resultado = "VITORIA"
            self.mensagem = "Dealer estourou! Você ganhou."
            self.saldo += self.aposta_atual * 2
        elif pts_player > pts_dealer_final:
            self.resultado = "VITORIA"
            self.mensagem = f"Você venceu! ({pts_player} vs {pts_dealer_final})"
            self.saldo += self.aposta_atual * 2
        elif pts_player < pts_dealer_final:
            self.resultado = "DERROTA"
            self.mensagem = f"A casa ganhou. ({pts_player} vs {pts_dealer_final})"
        else:
            self.resultado = "EMPATE"
            self.mensagem = "Push! Empate."
            self.saldo += self.aposta_atual

    def get_estado(self):
        if self.status == "JOGANDO":
            if self.mao_dealer:
                dealer_show = [self.mao_dealer[0], {'face': '🂠', 'valor': '?'}]
            else:
                dealer_show = []
        else:
            dealer_show = self.mao_dealer

        return {
            'player_hand': self.mao_jogador,
            'dealer_hand': dealer_show,
            'player_points': self.calcular_pontos(self.mao_jogador),
            'status': self.status,
            'resultado': self.resultado,
            'mensagem': self.mensagem,
            'saldo': self.saldo,
            'aposta': self.aposta_atual
        }