import pygame.midi
import time
import random
pygame.midi.init()

# http://www.ccarh.org/courses/253/handout/gminstruments/

player = pygame.midi.Output(0)
player.set_instrument(0, channel=2)


class midi_sound:
    def __init__(self, note, lifetime):
        self.life = 0
        self.lifetime = lifetime
        self.dead = False

        # Plays note
        self.note = note
        player.note_on(self.note, 50, channel=2)

    def run_lifetime(self):
        # Sets dead flag when lifetime is hit or exceeded
        self.life += 1
        if self.life >= self.lifetime:
            self.dead = True
            # Disables note when dead
            self.noteOff()

    def noteOff(self):
        # Disables note
        player.note_off(self.note, channel=2)


# Array of midi_node instance
NOTES = [midi_sound(random.randint(60, 120), random.randint(10000, 30000))]

good_notes = [0, 2, 4, 5, 7, 9, 11]

delay = .05

while True:

    # Iterates through notes
    for note in NOTES:
        # Calls lifetime count updater for each note
        note.run_lifetime()

        # After a note dies...
        if note.dead:
            ''' Changing delay '''
            if random.randint(1, 20) == 10:
                delay = random.randint(5, 10) / 100
                print("switched")

            ''' Enable For random delay between notes '''
            # time.sleep((6 ** (0.03 * (random.randint(1, 100) - 100)) / 1) / 2)
            ''' Constant Delay '''
            # time.sleep(.05)
            ''' Changing delay '''
            time.sleep(delay)


            # Adds a new note
            NOTES.append(midi_sound((60 + (random.randint(-1, 1) * 12)) + random.choice(good_notes), 60000))

    # Filters out dead notes
    NOTES = [note for note in NOTES if not note.dead]