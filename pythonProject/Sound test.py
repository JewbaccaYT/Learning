import pygame
import pygame.midi
import time

pygame.midi.init()
# pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
# sound = pygame.mixer.Sound("./sounds/1956.ogg")
# sound.play()

# game_of_life = pygame.mixer_music.load("./sounds/GOF.mp3")
# pygame.mixer.music.play()

player = pygame.midi.Output(0)

player.set_instrument(127, channel=2)

print('Playing...')
# Note 64 is E in the 5th Octave
player.note_on(36, 102, channel=2)
time.sleep(1)
player.note_off(36)

print('Played')

pygame.midi.quit()


# while True:

