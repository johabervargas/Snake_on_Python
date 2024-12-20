import pygame
import random

# Inicializando o Pygame
pygame.init()

# Configurações da tela
largura_tela = 600
altura_tela = 400
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Snake Game")

# Definindo cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Tamanho do bloco (cobra e comida)
tamanho_bloco = 20
velocidade = 10

# Relógio para controle da velocidade
relogio = pygame.time.Clock()

# Configurando fontes
fonte_pontuacao = pygame.font.SysFont("comicsansms", 35)
fonte_game_over = pygame.font.SysFont("comicsansms", 50)

def exibir_pontuacao(pontos):
    """Desenha a pontuação na tela."""
    texto = fonte_pontuacao.render(f"Pontuação: {pontos}", True, branco)
    tela.blit(texto, [10, 10])

def mensagem_game_over(pontuacao):
    """Exibe a mensagem de Game Over."""
    tela.fill(preto)
    texto_game_over = fonte_game_over.render("Game Over", True, vermelho)
    texto_pontuacao = fonte_pontuacao.render(f"Pontuação final: {pontuacao}", True, branco)
    texto_reiniciar = fonte_pontuacao.render("Pressione R para Reiniciar ou Q para Sair", True, branco)
    tela.blit(texto_game_over, [largura_tela // 2 - texto_game_over.get_width() // 2, altura_tela // 4])
    tela.blit(texto_pontuacao, [largura_tela // 2 - texto_pontuacao.get_width() // 2, altura_tela // 2])
    tela.blit(texto_reiniciar, [largura_tela // 2 - texto_reiniciar.get_width() // 2, altura_tela // 1.5])
    pygame.display.update()

def jogo():
    # Posição inicial da cobra
    x = largura_tela // 2
    y = altura_tela // 2
    movimento_x = 0
    movimento_y = 0

    # Inicializar posição aleatória da comida
    comida_x = random.randint(0, (largura_tela // tamanho_bloco) - 1) * tamanho_bloco
    comida_y = random.randint(0, (altura_tela // tamanho_bloco) - 1) * tamanho_bloco

    # Corpo da cobra e tamanho inicial
    corpo_cobra = []
    comprimento_cobra = 1

    # Pontuação inicial
    pontuacao = 0

    # Velocidade inicial dentro do jogo
    velocidade_atual = velocidade  # Velocidade ajustável

    # Flag para encerrar o jogo
    game_over = False

    while not game_over:
        # Verificar eventos de controle
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Verificar se a janela foi fechada
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:  # Movimentos da cobra
                if evento.key == pygame.K_LEFT and movimento_x == 0:
                    movimento_x = -tamanho_bloco
                    movimento_y = 0
                elif evento.key == pygame.K_RIGHT and movimento_x == 0:
                    movimento_x = tamanho_bloco
                    movimento_y = 0
                elif evento.key == pygame.K_UP and movimento_y == 0:
                    movimento_x = 0
                    movimento_y = -tamanho_bloco
                elif evento.key == pygame.K_DOWN and movimento_y == 0:
                    movimento_x = 0
                    movimento_y = tamanho_bloco

        # Atualizar posição da cobra
        x += movimento_x
        y += movimento_y

        # Verificar colisão com as bordas da tela
        if x < 0 or x >= largura_tela or y < 0 or y >= altura_tela:
            game_over = True

        # Verificar colisão com o próprio corpo
        for segmento in corpo_cobra[:-1]:
            if segmento == [x, y]:
                game_over = True

        # Verificar colisão com a comida
        if x == comida_x and y == comida_y:
            comprimento_cobra += 1
            pontuacao += 10

            # Aumentar a velocidade a cada 50 pontos
            if pontuacao % 50 == 0:
                velocidade_atual += 1

            # Reposicionar comida
            comida_x = random.randint(0, (largura_tela // tamanho_bloco) - 1) * tamanho_bloco
            comida_y = random.randint(0, (altura_tela // tamanho_bloco) - 1) * tamanho_bloco

        # Preencher o fundo
        tela.fill(preto)

        # Adicionar a nova posição da cabeça ao corpo
        corpo_cobra.append([x, y])

        # Manter o comprimento correto da cobra
        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]

        # Desenhar a cobra
        for segmento in corpo_cobra:
            pygame.draw.rect(tela, verde, [segmento[0], segmento[1], tamanho_bloco, tamanho_bloco])

        # Desenhar comida
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

        # Exibir a pontuação
        exibir_pontuacao(pontuacao)

        # Atualizar a tela
        pygame.display.update()

        # Controlar a velocidade
        relogio.tick(velocidade_atual)

    # Exibir a tela de Game Over
    mensagem_game_over(pontuacao)

    # Esperar reinício ou saída do jogo
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Reiniciar o jogo
                    jogo()
                elif evento.key == pygame.K_q:  # Sair do jogo
                    pygame.quit()
                    quit()

# Iniciar o jogo
jogo()
