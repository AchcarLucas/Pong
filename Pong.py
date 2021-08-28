import pygame

# define o tamanho da tela
screenSize = (800, 600)
# cria a tela e salva a instância dessa tela em screen
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Pong - Jogo")

# cria uma instância do time.Clock() - vamos usar para limitar o fps
gameClock = pygame.time.Clock()

# define o FPS do jogo
FPS = 60

# classe contendo as variaveis genericas do jogador e da máquina 
class GPlayer:
    # velocidade atual
    velocidade = 0

    # altura do jogador
    altura = 0

    # largura do jogador
    largura = 0

    # variavel de velocidade inicial
    velocidade_inicial = 0

    # variaveis de posição inicial
    x_inicial = 0
    y_inicial = 0

    # variaveis de posição do jogador
    x = 0
    y = 0

    # pontuação do player
    score = 0

variablesJogador = GPlayer()
variablesMaquina = GPlayer()

##########################
#       Jogador          #
##########################

# velocidade do jogador (1.0 / 60.0 é igual a 1 pixel por segundo)
variablesJogador.velocidade_inicial = 60.0 / FPS
variablesJogador.velocidade = variablesJogador.velocidade_inicial 

# altura do jogador
variablesJogador.altura = 65

# largura do jogador
variablesJogador.largura = 15

# posição x e y inicial (caso tenha um reset no jogo)
variablesJogador.x_inicial = 0
variablesJogador.y_inicial = (screenSize[1] / 2.0) - (variablesJogador.altura / 2.0)

# posição x e y do jogador (leva as posições iniciais)
variablesJogador.x = variablesJogador.x_inicial
variablesJogador.y = variablesJogador.y_inicial

##########################
#       Máquina          #
##########################

# velocidade da máquina (1.0 / 60.0 é igual a 1 pixel por segundo)
variablesMaquina.velocidade_inicial = 60.0 / FPS
variablesMaquina.velocidade = variablesMaquina.velocidade_inicial 

# altura da máquina
variablesMaquina.altura = 65

# largura da máquina
variablesMaquina.largura = 15

# posição inicial x da máquina (Tamanho da tela menos a largura da máquina)
variablesMaquina.x_inicial = screenSize[0] - variablesMaquina.largura
# posição inicial y da máquina (coloca no centro da altura da tela)
variablesMaquina.y_inicial = (screenSize[1] / 2.0) - (variablesMaquina.altura / 2.0)

# posição x e y da máquina (leva as posições iniciais)
variablesMaquina.x = variablesMaquina.x_inicial
variablesMaquina.y = variablesMaquina.y_inicial

class GBall:
    # velocidade atual da bola
    velocidade_x = 0
    velocidade_y = 0

    # direção do movimento (direita = 1 ou esquerda = -1)
    direcao = 0

    # raio da bola
    raio = 0

    # variaveis de posição inicial da bola
    x_inicial = 0
    y_inicial = 0

    # variaveis de posição da bola
    x = 0
    y = 0

##########################
#          Bola          #
##########################

variablesBola = GBall()
# define a velocidade inicial da bola
variablesBola.velocidade_x = 60.0 / FPS
variablesBola.velocidade_y = 60.0 / FPS

# direção
variablesBola.direcao = 1

# raio da bola
variablesBola.raio = 8

# salva a posição inicial da bola (para usar no reset)
variablesBola.x_inicial = screenSize[0] / 2.0
variablesBola.y_inicial = screenSize[1] / 2.0

variablesBola.x = variablesBola.x_inicial
variablesBola.y = variablesBola.y_inicial

def gameMain():
    # cria uma variavel que verifica se o jogo ainda está rodando
    gameRunning = True

    # verifica a cada frame se o jogo está rodando
    while gameRunning:
        screen.fill((0,0,0))

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
    global variablesJogador
    global variablesMaquina
    global variablesBola

    # verifica se alguma tecla esta sendo pressionada 
    key = pygame.key.get_pressed()

    # movimentação do jogador - subir e descer (leva em conta a velocidade do jogador e uma variação de tempo de dois frames)
    if(key[pygame.K_w] or key[pygame.K_UP]):
        variablesJogador.y = variablesJogador.y - variablesJogador.velocidade * deltaTime
    if(key[pygame.K_s] or key[pygame.K_DOWN]):
        variablesJogador.y = variablesJogador.y + variablesJogador.velocidade * deltaTime

    """ 
        detectar a colisão com as bordas da tela, só é necessário
        a verificação no eixo y já que não há movimentação do jogador
        e da máquina no eixo x
    """

    # verifica a colisão nas bordas da tela para o jogador
    if(variablesJogador.y <= 0):
        variablesJogador.y = 0
    elif(variablesJogador.y >= screenSize[1] - variablesJogador.altura):
        variablesJogador.y = screenSize[1] - variablesJogador.altura

    # verifica a colisão nas bordas da tela para a máquina
    if(variablesMaquina.y <= 0):
        variablesMaquina.y = 0
    elif(variablesMaquina.y >= screenSize[1] - variablesMaquina.altura):
        variablesMaquina.y = screenSize[1] - variablesMaquina.altura

# atualiza os gráficos na tela do jogo
def render(deltaTime):
    global variablesJogador
    global variablesMaquina
    global variablesBola

    # desenha o jogador
    pygame.draw.rect(screen, (255, 255, 255), (variablesJogador.x, variablesJogador.y, variablesJogador.largura, variablesJogador.altura))

    # desenha a máquina
    pygame.draw.rect(screen, (255, 255, 255), (variablesMaquina.x, variablesMaquina.y, variablesMaquina.largura, variablesMaquina.altura))

    # desenha a bola
    pygame.draw.circle(screen, (255, 255, 255), (variablesBola.x, variablesBola.y), variablesBola.raio)
    
# inicia o programa (chama o main)
gameMain()
