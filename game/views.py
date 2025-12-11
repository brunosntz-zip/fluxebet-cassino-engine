from django.shortcuts import render, redirect
from .engine import BlackjackEngine

jogo_atual = BlackjackEngine()

def index(request):
    global jogo_atual
    
    contexto = jogo_atual.get_estado()
    
    # Se o jogo ainda nem começou (estado inicial vazio), inicia
    if not contexto['player_hand'] and not contexto['dealer_hand']:
        jogo_atual.iniciar_jogo()
        contexto = jogo_atual.get_estado()

    return render(request, 'game/index.html', contexto)

def acao(request, tipo):
    global jogo_atual
    
    if tipo == 'hit':
        jogo_atual.hit()
    elif tipo == 'stand':
        jogo_atual.stand()
    elif tipo == 'reset':
        jogo_atual.iniciar_jogo()
        
    return redirect('index') # Recarrega a página