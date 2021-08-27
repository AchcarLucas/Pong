import pygame

#define o tamanho da tela
screenSize = (800, 600)
# cria a tela e salva a instância dessa tela em screen
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Pong - Jogo")

# cria uma instância do time.Clock() - vamos usar para limitar o fps
gameClock = pygame.time.Clock()

# define o FPS do jogo
FPS = 60

# velocidade do jogador (1.0 / 60.0 é igual a 1 pixel por segundo)
velocidadeJogador = 1.0 / FPS
# altura do jogador
alturaJogador = 10
# largura do jogador
larguraJogador = 40
# posição x do jogador
xJogador = 0
# posição y do jogador
yJogador = 0

# velocidade da máquina (1.0 / 60.0 é igual a 1 pixel por segundo)
velocidadeMaquina = 1.0 / FPS
# altura da máquina
alturaMaquina = 10
# largura da máquina
larguraMaquina = 40
# posição x da máquina
xMaquina = 0
# posição y da máquina
yMaquina = 0

def main():
    # cria uma variavel que verifica se o jogo ainda está rodando
    gameRunning = True

    # verifica a cada frame se o jogo está rodando
    while gameRunning:
        # limita o FPS em 60 quadros por segundo e salva o tempo que levou entre dois frames
        deltaTime = gameClock.tick(FPS)
    
        # verifica os eventos que estão na pool de eventos
        for event in pygame.event.get():
            # verifica se o X (da janela) foi pressionado, se sim, finalziada o jogo (gameRunning = False)
            if(event.type == pygame.QUIT):
                gameRunning = False
            # verifica se uma tecla foi pressionada
            if(event.type == pygame.KEYDOWN):
                # verifica se a tecla é o ESC, se sim, finaliza o jogo (gameRunning = False)
                if(event.key == pygame.K_ESCAPE):
                    gameRunning = False
            
        update(deltaTime)
        render(deltaTime)

        # depois que você definiu o que desenhar, faça a atualização da tela (chamamos essa parte de double-buffer)
        # o double-buffer evita flicks na tela
        pygame.display.update()

    # finaliza todos os módulos que foram iniciados
    pygame.quit()

# atualiza as ações lógicas do jogo
def update(deltaTime):
    pass

# atualiza os gráficos na tela do jogo
def render(deltaTime):
    # desenha o jogador
    pygame.draw.rect(screen, (255, 255, 255), (xJogador, yJogador, alturaJogador, larguraJogador))

    # desenha a máquina
    pygame.draw.rect(screen, (255, 255, 255), (xMaquina, yMaquina, alturaMaquina, larguraMaquina))
    
# inicia o programa (chama o main)
main()
