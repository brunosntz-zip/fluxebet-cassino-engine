import random

class BlackjackEngine:
    def __init__(self):
        self.baralho = []
        self.mao_jogador = []
        self.mao_dealer = []
        self.status = "AGUARDANDO" # AGUARDANDO, JOGANDO, FINALIZADO
        self.resultado = "" # VITORIA, DERROTA, EMPATE
        self.mensagem = ""
    
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
        if len(self.baralho) < 1:
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

    def iniciar_jogo(self):
        self.criar_baralho()
        self.mao_jogador = [self.dar_carta(), self.dar_carta()]
        self.mao_dealer = [self.dar_carta(), self.dar_carta()]
        self.status = "JOGANDO"
        self.resultado = ""
        self.mensagem = "Jogo iniciado! Hit ou Stand?"
        
        # Checa Blackjack imediato
        pts_player = self.calcular_pontos(self.mao_jogador)
        if pts_player == 21:
            self.finalizar_turno_dealer()

        return self.get_estado()

    def hit(self):
        if self.status != "JOGANDO":
            return self.get_estado()
            
        carta = self.dar_carta()
        self.mao_jogador.append(carta)
        
        pts = self.calcular_pontos(self.mao_jogador)
        if pts > 21:
            self.status = "FINALIZADO"
            self.resultado = "DERROTA"
            self.mensagem = "Estourou (Bust)! A casa ganha."
        
        return self.get_estado()

    def stand(self):
        if self.status != "JOGANDO":
            return self.get_estado()
        self.finalizar_turno_dealer()
        return self.get_estado()

    def finalizar_turno_dealer(self):
        self.status = "FINALIZADO"
        while self.calcular_pontos(self.mao_dealer) < 17:
            self.mao_dealer.append(self.dar_carta())
            
        pts_player = self.calcular_pontos(self.mao_jogador)
        pts_dealer = self.calcular_pontos(self.mao_dealer)
        
        if pts_player > 21:
            self.resultado = "DERROTA"
            self.mensagem = "Você estourou."
        elif pts_dealer > 21:
            self.resultado = "VITORIA"
            self.mensagem = "Dealer estourou! Você ganhou."
        elif pts_player > pts_dealer:
            self.resultado = "VITORIA"
            self.mensagem = f"Você venceu! ({pts_player} vs {pts_dealer})"
        elif pts_player < pts_dealer:
            self.resultado = "DERROTA"
            self.mensagem = f"A casa ganhou. ({pts_player} vs {pts_dealer})"
        else:
            self.resultado = "EMPATE"
            self.mensagem = "Push! Empate."

    def get_estado(self):
        # Lógica de Proteção: O Dealer tem cartas?
        if not self.mao_dealer:
            dealer_display = []
        elif self.status == "FINALIZADO":
            dealer_display = self.mao_dealer # Mostra tudo
        else:
            # Esconde a segunda carta
            dealer_display = [self.mao_dealer[0], {'face': '🂠', 'valor': '?'}]

        return {
            'player_hand': self.mao_jogador,
            'dealer_hand': dealer_display,
            'player_points': self.calcular_pontos(self.mao_jogador),
            'status': self.status,
            'resultado': self.resultado,
            'mensagem': self.mensagem
        }