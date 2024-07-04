import pygame, random
from pygame.locals import *

pygame.init()

GAME_NAME = 'Tic Tac Toe'
SCREEN_SIZE = pygame.math.Vector2(600, 640)
BACKGROUND_COLOR = '#222222'
BOARD_SIZE = 3
SCENE = 'START MENU'

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(SCREEN_SIZE, SCALED)
        pygame.display.set_caption(GAME_NAME)
        self.event_map = set()
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = X

    def update_event_map(self):
        self.event_map.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.event_map.add(QUIT)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.event_map.add(MOUSEBUTTONDOWN)

    def run(self):
        global SCENE
        return_button = Button('Return', pygame.font.Font(None, 30), 'white',
                               (100, 50), (60,40), BACKGROUND_COLOR, 0,
                               0, 'white', 3, 25)
        while True:
            self.update_event_map()
            if QUIT in self.event_map: break

            self.screen.fill(BACKGROUND_COLOR)

            if SCENE == 'START MENU':
                StartMenu.render(self.screen)
                StartMenu.button_clicked()
            elif SCENE in {'VS PLAYER', 'VS COMPUTER'}:
                return_button.render(self.screen)
                if return_button.clicked():
                    self.clear_board()
                    SCENE = 'START MENU'
                if SCENE == 'VS COMPUTER' and self.current_player == O:
                    ComputerMove.play(self)
                    self.play()
                self.put_player()
                self.play()
                
            elif SCENE == 'COMPUTER MENU':
                return_button.render(self.screen)
                if return_button.clicked(): SCENE = 'START MENU'
                ComputerMenu.render(self.screen)
                ComputerMenu.button_clicked()

            pygame.display.flip()

        pygame.quit()

    def play(self):
        self.render_grids()
        self.render_player()
        if self.is_win(self.next_player().value):
            self.render_text(f'{self.current_player.name} win!', self.current_player.color)
        elif self.is_board_full():
            self.render_text('Tie...', 'white')

    def clear_board(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = X

    def is_board_full(self) -> bool:
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def is_win(self, player: int) -> bool:
        for i in range(BOARD_SIZE):
            hor = ver = diag1 = diag2 = 0
            for j in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    hor += 1
                if self.board[j][i] == player:
                    ver += 1
                if self.board[j][j] == player:
                    diag1 += 1
                if self.board[j][BOARD_SIZE - j - 1] == player:
                    diag2 += 1
            if 3 in [hor, ver, diag1, diag2]:
                self.current_player = self.next_player()
                return True
        return False
    
    def render_grids(self):
        for i in range(2, BOARD_SIZE + 1):
            pygame.draw.line(self.screen, 'white', (120, 40 + 120*i), (120 * 4, 40 + 120 * i), 10)
            pygame.draw.line(self.screen, 'white', (120 * i, 160), (120 * i, 40 + 120 * 4), 10)

    def render_player(self):
        for i in range(1, BOARD_SIZE + 1):
            for j in range(1, BOARD_SIZE + 1):
                player = self.board[i-1][j-1]
                if player == X.value:
                    X.rect.topleft = (120*i + 20, 120*j + 20 + 40)
                    X.draw(self.screen)
                elif player == O.value:
                    O.rect.topleft = (120*i + 20, 120*j + 20 + 40)
                    O.draw(self.screen)

    def put_player(self):
        if MOUSEBUTTONDOWN not in self.event_map: return
        mous_pos = pygame.mouse.get_pos()
        if mous_pos[0] < 120 or mous_pos[0] > 120 * 4 or mous_pos[1] < 160 or mous_pos[1] > 40 + 120 * 4: return
        row = int((mous_pos[0] - 120) / 120)
        col = int((mous_pos[1] - 40 - 120) / 120)
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player.value
            self.current_player = self.next_player()

    def next_player(self):
        return O if self.current_player == X else X

    def render_text(self, text: str, color: str, font=pygame.font.Font(None, 100)):
        f_surf = font.render(text, True, color)
        f_rect = f_surf.get_rect(midtop=(SCREEN_SIZE.x // 2, 60))
        self.screen.blit(f_surf, f_rect)
        pygame.display.update(f_rect)
        pygame.time.wait(2000)
        self.clear_board()

class Button:
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 color: str,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 background: str,
                 radius: int = -1,
                 border_spacing: int = -1,
                 border_color: str = '',
                 border_width: int = 0,
                 border_radius: int = -1) -> None:
    
        self.surf = pygame.Surface(size, SRCALPHA)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, background, self.rect, border_radius=radius)

        if border_spacing != -1 and border_color:
            pygame.draw.rect(self.surf,
                            border_color,
                            pygame.Rect(border_spacing,
                                        border_spacing,
                                        self.rect.width - 2 * border_spacing,
                                        self.rect.height - 2 * border_spacing),
                            border_width,
                            border_radius)

        f_surf = font.render(text, True, color)
        f_rect = f_surf.get_rect(center=self.rect.center)
        self.surf.blit(f_surf, f_rect)

        self.rect.center = pos

    def hovred(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def clicked(self) -> bool:
        if self.hovred() and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(200)
            return True
        return False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, self.rect)

class StartMenu:
    style = (pygame.font.Font(None, 50), 'white',
             (300, 90), [SCREEN_SIZE.x // 2, 0], BACKGROUND_COLOR, 50,
             0, 'white', 5, 50)
    style[3][1] = 250
    vs_player = Button('VS Player', *style)
    style[3][1] = 380
    vs_computer = Button('VS Computer', *style)

    def render(surface):
        StartMenu.vs_computer.render(surface)
        StartMenu.vs_player.render(surface)

    def button_clicked():
        global SCENE
        if StartMenu.vs_player.clicked(): SCENE = 'VS PLAYER'
        elif StartMenu.vs_computer.clicked(): SCENE = 'COMPUTER MENU'

class ComputerMenu:
    style = (pygame.font.Font(None, 50), 'white',
            (200, 90), [SCREEN_SIZE.x // 2, 0], BACKGROUND_COLOR, 50,
            0, 'white', 5, 50)
    style[3][1] = 180
    easy = Button('Easy', *style)
    style[3][1] = 300
    medium = Button('Medium', *style)
    style[3][1] = 420
    hard = Button('Hard', *style)

    @staticmethod
    def render(surface):
        ComputerMenu.easy.render(surface)
        ComputerMenu.medium.render(surface)
        ComputerMenu.hard.render(surface)

    @staticmethod
    def button_clicked():
        global SCENE
        if ComputerMenu.easy.clicked():
            SCENE = 'VS COMPUTER'
            ComputerMove.level = 'EASY'
        elif ComputerMenu.medium.clicked():
            SCENE = 'VS COMPUTER'
            ComputerMove.level = 'MEDIUM'
        elif ComputerMenu.hard.clicked():
            SCENE = 'VS COMPUTER'
            ComputerMove.level = 'HARD'

class X:
    name = 'X'
    value = 1
    color = 'blue'
    surf = pygame.Surface((80, 80), SRCALPHA)
    rect = surf.get_rect()
    pygame.draw.line(surf, color, (0,0), (80,80), 20)
    pygame.draw.line(surf, color, (0,80), (80,0), 20)

    @staticmethod
    def __eq__(other: object) -> bool:
        return X.value == other.value

    @staticmethod
    def draw(surface: pygame.Surface):
        surface.blit(X.surf, X.rect)

class O:
    name = 'O'
    value = -1
    color = 'red'
    surf = pygame.Surface((80, 80), SRCALPHA)
    rect = surf.get_rect()
    pygame.draw.circle(surf, color, (40,40), 40, 10)

    @staticmethod
    def __eq__(other: object) -> bool:
        return O.value == other.value

    @staticmethod
    def draw(surface: pygame.Surface):
        surface.blit(O.surf, O.rect)

class ComputerMove:
    level = ''

    @staticmethod
    def play(game: Game):
        if ComputerMove.level == 'EASY':
            ComputerMove.easy(game)
        elif ComputerMove.level == 'MEDIUM':
            ComputerMove.medium(game)
        else:
            ComputerMove.hard(game)
        game.current_player = X
        pygame.time.wait(100)

    @staticmethod
    def easy(game: Game):
        while True:
            i = random.randint(0, BOARD_SIZE - 1)
            j = random.randint(0, BOARD_SIZE - 1)
            if game.board[i][j] == 0:
                game.board[i][j] = O.value
                break

    @staticmethod
    def medium(game: Game):
        best_move = None
        best_score = float('-inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if game.board[i][j] != 0: continue
                game.board[i][j] = O.value
                score = ComputerMove.minimax(game, depth=4)
                game.board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i,j)
        if best_move: game.board[best_move[0]][best_move[1]] = O.value
        else: ComputerMove.easy(game)

    @staticmethod
    def hard(game: Game):
        best_move = None
        best_score = float('-inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if game.board[i][j] != 0: continue
                game.board[i][j] = O.value
                score = ComputerMove.minimax(game)
                game.board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i,j)
        game.board[best_move[0]][best_move[1]] = O.value

    @staticmethod
    def minimax(game: Game, is_max: bool = False, depth: int = float('inf')):
        if game.is_win(O.value): return float('inf')
        if game.is_win(X.value): return float('-inf')
        if game.is_board_full() or depth <= 0: return 0
        
        if is_max:
            best_score = float('-inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if game.board[i][j] != 0: continue
                    game.board[i][j] = O.value
                    score = ComputerMove.minimax(game, False, depth - 1)
                    game.board[i][j] = 0
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if game.board[i][j] != 0: continue
                    game.board[i][j] = X.value
                    score = ComputerMove.minimax(game, True, depth - 1)
                    game.board[i][j] = 0
                    best_score = min(score, best_score)
            return best_score


if __name__ == '__main__':
    Game().run()
