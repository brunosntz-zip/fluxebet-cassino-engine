from django.shortcuts import render, redirect
from .engine import BlackjackEngine

jogo_atual = BlackjackEngine()

def index(request):
    return render(request, 'game/index.html', jogo_atual.get_estado())

def acao(request, tipo):
    global jogo_atual
    
    if tipo == 'hit':
        jogo_atual.hit()
    elif tipo == 'stand':
        jogo_atual.stand()
    elif tipo == 'double':
        jogo_atual.double()
    elif tipo == 'reset':
        jogo_atual.status = "APOSTANDO"
    elif tipo == 'add_money':
        jogo_atual.adicionar_saldo()

    return redirect('/#mesa-de-jogo')

def apostar(request):
    if request.method == 'POST':
        valor = int(request.POST.get('valor_aposta'))
        jogo_atual.apostar(valor)
    return redirect('/#mesa-de-jogo')