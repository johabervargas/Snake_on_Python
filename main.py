import pygame
import random
import xml.etree.ElementTree as ET

# Configurações iniciais
largura_tela = 640
altura_tela = 480
tamanho_bloco = 20
preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

# Função para salvar a pontuação em um arquivo XML
def salvar_pontuacao(pontuacao_max):
    """Salva a pontuação no arquivo XML."""
    try:
        tree = ET.parse('pontuacao.xml')
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element("pontuacoes")
        tree = ET.ElementTree(root)

    # Encontrar a pontuação mais alta
    pontuacao_max_elem = root.find("pontuacao_max")
    
    # Se não existir, cria o elemento
    if pontuacao_max_elem is None:
        pontuacao_max_elem = ET.SubElement(root, "pontuacao_max")
    
    # Atualiza a pontuação máxima se a pontuação atual for maior
    if int(pontuacao_max_elem.text) < pontuacao_max:
        pontuacao_max_elem.text = str(pontuacao_max)
    
    # Salva o arquivo XML
    tree.write('pontuacao.xml')

# Função para carregar a pontuação de um arquivo XML
def carregar_pontuacao():
    """Carrega a pontuação mais alta do arquivo XML."""
    try:
        tree = ET.parse('pontuacao.xml')
        root = tree.getroot()
        pontuacao_max_elem = root.find("pontuacao_max")
        return int(pontuacao_max_elem.text) if pontuacao_max_elem is not None else 0
    except FileNotFoundError:
        return 0  # Caso o arquivo não exista, retorna 0

# Função para exibir a pontuação na tela
def exibir_pontuacao(pontuacao, font, tela):
    texto_pontuacao = font.render(f"Pontuação: {pontuacao}", True, branco)
    tela.blit(texto_pontuacao, [10, 10])

# Função para exibir a pontuação máxima na tela
def exibir_pontuacao_maxima(pontuacao_max, font, tela):
    texto_pontuacao_maxima = font.render(f"Pontuação Máxima: {pontuacao_max}", True, branco)
    tela.blit(texto_pontuacao_maxima, [largura_tela // 2 - 100, 10])

# Função para exibir a mensagem de game over
def mensagem_game_over(pontuacao, font, tela):
    texto_game_over = font.render(f"Fim de Jogo! Pontuação Final: {pontuacao}", True, vermelho)
    tela.blit(texto_game_over, [largura_tela // 4, altura_tela // 3])
    texto_opcoes = font.render("Pressione 'R' para Recomeçar ou 'Q' para Sair", True, branco)
    tela.blit(texto_opcoes, [largura_tela // 4, altura_tela // 2])

# Função principal do jogo
def jogo(pontuacao_max):
    pygame.init()

    # Configura a tela do jogo
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Snake Game')

    # Fonte
    font = pygame.font.SysFont("arial", 25)

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

    # Flag para encerrar o jogo
    game_over = False

    # Loop principal do jogo
    while not game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    movimento_x = -tamanho_bloco
                    movimento_y = 0
                elif evento.key == pygame.K_RIGHT:
                    movimento_x = tamanho_bloco
                    movimento_y = 0
                elif evento.key == pygame.K_UP:
                    movimento_y = -tamanho_bloco
                    movimento_x = 0
                elif evento.key == pygame.K_DOWN:
                    movimento_y = tamanho_bloco
                    movimento_x = 0

        # Movimento da cobra
        x += movimento_x
        y += movimento_y

        # Verificar colisão com as bordas
        if x < 0 or x >= largura_tela or y < 0 or y >= altura_tela:
            game_over = True

        # Adicionar nova posição ao corpo da cobra
        corpo_cobra.append([x, y])
        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]

        # Verificar colisão com o próprio corpo
        for bloco in corpo_cobra[:-1]:
            if bloco == [x, y]:
                game_over = True

        # Verificar colisão com a comida
        if x == comida_x and y == comida_y:
            comprimento_cobra += 1
            comida_x = random.randint(0, (largura_tela // tamanho_bloco) - 1) * tamanho_bloco
            comida_y = random.randint(0, (altura_tela // tamanho_bloco) - 1) * tamanho_bloco
            pontuacao += 10

        # Atualizar a tela
        tela.fill(preto)

        # Exibir a pontuação e a pontuação máxima
        exibir_pontuacao(pontuacao, font, tela)
        exibir_pontuacao_maxima(pontuacao_max, font, tela)

        # Desenhar a cobra
        for bloco in corpo_cobra:
            pygame.draw.rect(tela, verde, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

        # Desenhar a comida
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

        # Atualizar a tela
        pygame.display.update()

        # Controlar o FPS
        pygame.time.Clock().tick(15)

        # Verificar se a pontuação atual é maior que a máxima
        if pontuacao > pontuacao_max:
            pontuacao_max = pontuacao  # Atualizar pontuação máxima

    # Mensagem de game over
    while game_over:
        tela.fill(preto)
        mensagem_game_over(pontuacao, font, tela)
        
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Recomeçar
                    jogo(pontuacao_max)  # Chama novamente a função jogo() para reiniciar
                elif evento.key == pygame.K_q:  # Sair
                    pygame.quit()
                    quit()

    # Salvar a pontuação mais alta quando o jogo acabar
    salvar_pontuacao(pontuacao_max)

# Rodar o jogo
if __name__ == "__main__":
    pontuacao_max = carregar_pontuacao()  # Carregar a pontuação máxima ao iniciar o jogo
    jogo(pontuacao_max)
