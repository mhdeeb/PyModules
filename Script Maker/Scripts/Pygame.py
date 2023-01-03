import pygame

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Script")
    clock = pygame.time.Clock()

    while True:
        window.fill('black')
        pygame.draw.rect(window, (255, 0, 0), (0, 0, 100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clock.tick(60)
        pygame.display.update()
