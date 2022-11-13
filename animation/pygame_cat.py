import pygame
import glob
 
SIZE = WIDTH, HEIGHT = 600, 600 #the width and height of our screen
FPS = 9 #Frames per second
 
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
 
        self.images = [pygame.image.load(img) for img in glob.glob("Storytube/pygame/cat/*.png")]
        self.index = 0
        self.rect = pygame.Rect(5, 5, 150, 198)
 
    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1
 
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Trace")
    my_sprite = MySprite()
    my_group = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
 
        my_group.update()
        screen.fill((0,0,0))
        my_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
 
if __name__ == '__main__':
    main()