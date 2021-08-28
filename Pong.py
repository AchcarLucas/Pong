import pygame
import random
import math

# define o tamanho da tela
screenSize = (800, 600)
# cria a tela e salva a instância dessa tela em screen
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Pong - Jogo")

# inicializa a fonte
pygame.font.init()

# carrega uma fonte padrão (Arial)
gameFont = pygame.font.SysFont("Arial", 35)

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
variablesJogador.velocidade_inicial = 30.0 / FPS
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
variablesMaquina.velocidade_inicial = 40.0 / FPS
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

    # direção da bola
    dir = 0

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

randomAngle = math.pi / 4

variablesBola = GBall()

# raio da bola
variablesBola.raio = 8

# salva a posição inicial da bola (para usar no reset)
variablesBola.x_inicial = screenSize[0] / 2.0
variablesBola.y_inicial = screenSize[1] / 2.0

def resetBall():
    # coloca a bola no centro da tela novamente
    variablesBola.x = variablesBola.x_inicial
    variablesBola.y = variablesBola.y_inicial

    # randomiza o cone de lançamento
    angleRand = (math.pi / 2) + random.uniform(-randomAngle, randomAngle)

    # inicializa uma direção
    randDir = 1

    # randomiza a direção (se entrar no if, inverte a direção)
    if(random.uniform(0, 1) >= 0.5):
        randDir = -1

    # salva a direção na bola
    variablesBola.dir = randDir

    # randomiza a velocidade inicial (0.3 até 0.8)
    randVelocity = random.uniform(0.3, 0.8)

    # inicia o cone de lançamento da bola
    variablesBola.velocidade_x = randDir * randVelocity *  math.sin(angleRand)
    variablesBola.velocidade_y = randVelocity * math.cos(angleRand)

def revertBall():
    # reverte a direção da bola
    variablesBola.dir = (-1.0) * variablesBola.dir

    # randomiza uma velocidade inicial
    randVelocity = random.uniform(0.3, 0.8)

    # randomiza o ângulo de lançamento
    angleRand = (math.pi / 2) + random.uniform(-randomAngle, randomAngle)

    # inicia a nova velocidade
    variablesBola.velocidade_x = variablesBola.dir * randVelocity *  math.sin(angleRand)
    variablesBola.velocidade_y = randVelocity * math.cos(angleRand)

# faz um reset nas configurações bola antes de iniciar o jogo
resetBall()

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

    # verifica se alguma tecla esta sendo pressionada 
    key = pygame.key.get_pressed()

    '''
        detecta as key e modifica a posição do jogador
    '''

    # movimentação do jogador - subir e descer (leva em conta a velocidade do jogador e uma variação de tempo de dois frames)
    if(key[pygame.K_w] or key[pygame.K_UP]):
        variablesJogador.y = variablesJogador.y - variablesJogador.velocidade * deltaTime
    if(key[pygame.K_s] or key[pygame.K_DOWN]):
        variablesJogador.y = variablesJogador.y + variablesJogador.velocidade * deltaTime

    '''
       movimentação da máquina (segue a bola sempre)
       a dificuldade da máquina é definido pela altura da base e sua velocidade
    '''

    # cria uma variabel temporária que determina o centro em y da barra
    tmp_center = variablesMaquina.y + (variablesMaquina.altura / 2.0)
    # cria uma variavel temporária da velocidade
    tmp_velocity = variablesMaquina.velocidade

    # verifica se o centro da barra é maior que a posição y da bola (se for, movimenta a máquina para baixo)
    if(tmp_center >= variablesBola.y):
        # se a diferença a bola até o centro for do tamanho da bola, diminua a velocidade proporcionalmente
        if(math.fabs(variablesBola.y - tmp_center) < variablesMaquina.altura):
            tmp_velocity = tmp_velocity*math.fabs(variablesBola.y - tmp_center) / variablesMaquina.altura
        # movimenta a barra
        variablesMaquina.y = variablesMaquina.y - tmp_velocity * deltaTime
    # aqui acontece o contrário, se a posição do centro for menor que y da bola, movimenta para cima
    elif(tmp_center <= variablesBola.y):
        # se a diferença a bola até o centro for do tamanho da bola, diminua a velocidade proporcionalmente
        if(math.fabs(variablesBola.y - tmp_center) < variablesMaquina.altura):
            tmp_velocity = tmp_velocity*math.fabs(variablesBola.y - tmp_center) / variablesMaquina.altura
        # movimenta a barra
        variablesMaquina.y = variablesMaquina.y + tmp_velocity * deltaTime

    '''
        Essa parte do código faz a movimentação da bola e detecção de colisão
        da bola com o jogador e a máquina
    '''

    # movimenta a bola em x e y
    variablesBola.x = variablesBola.x + variablesBola.velocidade_x * deltaTime
    variablesBola.y = variablesBola.y - variablesBola.velocidade_y * deltaTime

    # cria rect do jogador, máquina e da bola para utilizar com a função colliderect do módulo Rect
    rectJogador = pygame.Rect((variablesJogador.x, variablesJogador.y, variablesJogador.largura, variablesJogador.altura))
    rectMaquina = pygame.Rect((variablesMaquina.x, variablesMaquina.y, variablesMaquina.largura, variablesMaquina.altura))
    rectBola    = pygame.Rect((variablesBola.x, variablesBola.y, variablesBola.raio, variablesBola.raio))

    # verifica se a bola colidiu com o jogador ou máquina, se sim, modifica a direção da bola com novos parametros
    # a verificação da dir é necessário para não ocorrer mais de uma detecção de colisão
    if(pygame.Rect.colliderect(rectJogador, rectBola) and variablesBola.dir == -1):
        # revert o lance com um novo cone de lançamento
        revertBall()
    elif(pygame.Rect.colliderect(rectMaquina, rectBola) and variablesBola.dir == 1):
        # revert o lance com um novo cone de lançamento
        revertBall()
    '''
        Essa parte do código detecta se ocorreu uma bola fora
        se sim, reseta a bola da os pontos ao jogador e inicia
        uma nova jogada
    '''

    # verifica se ocorreu alguma colisão nas laterais esquerda ou direita
    if(variablesBola.x >= screenSize[0] + 2 * variablesBola.raio):
        # reseta a bola
        resetBall()
        # adiciona um ponto ao jogador
        variablesJogador.score = variablesJogador.score + 1
    elif(variablesBola.x <= (-1) * 2 * variablesBola.raio):
        # reseta a bola
        resetBall()
        # adiciona um ponto a máquina
        variablesMaquina.score = variablesMaquina.score + 1

    """ 
        detectar a colisão com as bordas da tela do jogador máquina e da bola.

        para a máquina e o jogador, só é necessário a verificação no eixo y já que não há movimentação do jogador
        e da máquina no eixo x.

        para a bola, só é necessário verificar a colisão na parte inferior e superior e reverter a velocidade no
        eixo y

    """

     # verifica as colisões das bordas superior e inferior (reverte a velocidade y se ocorrer colisão)
    if(variablesBola.y >= screenSize[1] - variablesBola.raio or variablesBola.y <= 0):
        variablesBola.velocidade_y = (-1)*variablesBola.velocidade_y

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
    # desenha o jogador
    pygame.draw.rect(screen, (255, 255, 255), (variablesJogador.x, variablesJogador.y, variablesJogador.largura, variablesJogador.altura))

    # desenha a máquina
    pygame.draw.rect(screen, (255, 255, 255), (variablesMaquina.x, variablesMaquina.y, variablesMaquina.largura, variablesMaquina.altura))

    # desenha a bola
    pygame.draw.circle(screen, (255, 255, 255), (variablesBola.x, variablesBola.y), variablesBola.raio)

    # desenha a linha central
    pygame.draw.line(screen, (255, 255, 255), (screenSize[0] / 2.0, 0), (screenSize[0] / 2.0, screenSize[1]))

    # cria uma surface da fonte com a escrita que a gente quer
    scoreJogador = gameFont.render(f"Score: {variablesJogador.score}", 1, (255, 255, 255))
    scoreMaquina = gameFont.render(f"Score: {variablesMaquina.score}", 1, (255, 255, 255))

    # desenha as surfaces dos textos
    screen.blit(scoreJogador, (10, 10))
    screen.blit(scoreMaquina, (screenSize[0] - scoreMaquina.get_width() - 10, 10))
    
# inicia o programa (chama o main)
gameMain()
