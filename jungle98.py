#! python3
# jungle98.py

import os
import pygame
import sys
from pygame.locals import *

# objects
sequence_number = 16
blockSizex = 50
blockSizey = 50
# system variables
title = 'jungle98'
audioSettings = {"frequency": 44100, "size": -16, "channels": 2, "buffer": 2048}
window_size = {"width": blockSizex * (sequence_number + 1), "height": blockSizey * 14}
# sounds sequences
project_name = "Solar_Glide"
# tempo = 168
# objects 2
system_fps = 60
s_tempo = 9
# mixer inits
pygame.mixer.pre_init(
    audioSettings["frequency"],
    audioSettings["size"],
    audioSettings["channels"],
    audioSettings["buffer"],
)
pygame.mixer.init()
pygame.init()
# Colors
black_color = (0, 0, 0)
white_color = (200, 200, 200)
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((
    window_size["width"],
    window_size["height"]))
pygame.display.set_caption(title)
# font settings
font = pygame.font.SysFont(None, 18)
# _empty_bar =  pygame.Rect(2, window_size["height"] - blockSize, 0, 0) # pygame.image.load("images/bar.png").convert()
# time_bar = pygame.draw.rect(window_surface, white_color, _empty_bar, 0)

# bar image load
time_bar_image = pygame.image.load('images/bar.png').convert()
time_bar = time_bar_image.get_rect()
# bak image load
bak_image = pygame.image.load('images/bak.png').convert()
bak_bar= bak_image.get_rect()
# drum memories
_jsonPath = "./" + project_name + "/breaks/meta.json"
with open(_jsonPath, encoding="utf-8", mode="r") as f:
    import json
    d = json.load(f)
# load sounds
break_list = []
for json in d:
    break_list.append("./" + project_name + "/breaks/" + json["data"])
print(break_list)

# ambient memories
_jsonPath = "./" + project_name + "/ambient/meta.json"
with open(_jsonPath, encoding="utf-8", mode="r") as f:
    import json
    d = json.load(f)
# load sounds
sample1_list = []
sample2_list = []
for json in d:
    if json["sample1"] == True:
        sample1_list.append("./" + project_name + "/ambient/" + json["data"])
    else:
        sample2_list.append("./" + project_name + "/ambient/" + json["data"])

class SoundSquare:
    def __init__(self, audio_file, x_pos, y_pos, track_num):
        self.sizex = blockSizex
        self.sizey = blockSizey
        self.off = pygame.image.load("images/off.png").convert_alpha()
        self.on = pygame.image.load("images/on.png").convert_alpha()
        self._state = False
        self.rect = pygame.Rect(x_pos, y_pos, self.sizex, self.sizey)
        self.sound = pygame.mixer.Sound(audio_file)
        self.sound.set_volume(0.6)

    def get_state(self):
        return self._state

    def toggle_state(self):
        self._state = not self._state

    def render(self):
        if self._state is False:
            window_surface.blit(self.off, self.rect)
        else:
            window_surface.blit(self.on, self.rect)

def change_state(sound_square):
    mouse_pos = pygame.mouse.get_pos()
    if sound_square.rect.collidepoint(mouse_pos):
        sound_square.toggle_state()

# Text rendering
def render_text():
    x = (blockSizex) / 2
    y = (blockSizey) / 2

    # main picture
    y += float(window_size["height"]) * 2 / float(len(break_list) + 6)

    # mod
    render_text = font.render("mod:     activated", True, white_color)
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)
    y += float(window_size["height"]) / float(len(break_list) + 6)

    for i in range(len(break_list)):
        render_text = font.render("bre" + str(i + 1), True, white_color)
        render_text_rect = render_text.get_rect(center=(x, y))
        window_surface.blit(render_text, render_text_rect)
        y += float(window_size["height"]) / float(len(break_list) + 6)
    # s1
    render_text = font.render("sam1:     sample1-168-1.wav", True, white_color)
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)
    y += float(window_size["height"]) / float(len(break_list) + 6)

    # s2
    render_text = font.render("sam2:     deactivated", True, white_color)
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)
    y += float(window_size["height"]) / float(len(break_list) + 6)

def terminate():
    pygame.quit()
    sys.exit()

def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# Check for collision between time bar and 'on' sound square
def collide(time_bar, track_list):
    for track in track_list:
        for sound_square in track:
            if time_bar.right >= sound_square.rect.left -4 and time_bar.right <= sound_square.rect.left +4:
                if sound_square._state == True:
                    sound_square.sound.play()


# set up sound squares
track_list = []
for j in range(len(break_list)):
    track_list.append([])
    for i in range(0, sequence_number):
        sound_square = SoundSquare(break_list[j], blockSizex * (i+ 1), blockSizey * (j+ 3) , j)
        track_list[j].append(sound_square)

# set up ambients
selected_sample1 = 0
selected_sample2 = -1
sample1_data = []
sample2_data = []
for j in range(len(sample1_list)):
    sound_square = pygame.mixer.Sound(sample1_list[j])
    sample1_data.append(sound_square)
for j in range(len(sample2_list)):
    sound_square = pygame.mixer.Sound(sample2_list[j])
    sample2_data.append(sound_square)

time_bar.right = blockSizex
time_bar.top = blockSizey * 3

where_half = 0 # 0 -> 8 -> 16

# play only sample
if selected_sample1 != -1:
    sample1_data[selected_sample1].play()
if selected_sample2 != -1:
    sample2_data[selected_sample2].play()

while True:
    dt = main_clock.tick(float(system_fps))
    on_list = []

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for track in track_list:
                for sound_square in track:
                    change_state(sound_square)

    if time_bar.right > window_size["width"] - s_tempo -1:
        time_bar.right = blockSizex -s_tempo
        where_half += 8

        if(where_half & 8 == 0):
            if selected_sample1 != -1:
                sample1_data[selected_sample1].play()
            if selected_sample2 != -1:
                sample2_data[selected_sample2].play()


    print(float(dt))
    time_bar.move_ip(float(s_tempo * (float(dt if dt >= 14 and dt <= 18 else 17)) / 16.0), 0)
    window_surface.fill(black_color)
    for track in track_list:
        for sound_square in track:
            sound_square.render()

    render_text()
    collide(time_bar, track_list)

    window_surface.blit(time_bar_image, time_bar)
    window_surface.blit(bak_image, bak_bar)

    pygame.display.update()
    main_clock.tick(system_fps)
