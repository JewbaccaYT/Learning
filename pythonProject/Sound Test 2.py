import pygame
import pygame.midi
pygame.midi.init()

player = pygame.midi.Output(0)
player.set_instrument(119, channel=2)

print('Playing...')
# Note 64 is E in the 5th Octave
player.note_on(36, 102, channel=2)
time.sleep(1)
player.note_off(36)

print('Played')

pygame.midi.quit()

