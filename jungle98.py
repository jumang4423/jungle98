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
title = "jungle98"
audioSettings = {"frequency": 44100, "size": -16, "channels": 2, "buffer": 2048}
window_size = {"width": blockSizex * (sequence_number + 1), "height": blockSizey * 14}
# sounds sequences
project_name = "solar_glide"
tempo = 149
# objects 2
system_fps = 60.0
s_tempo = 4 * (
    16 / sequence_number
)  # float(blockSizex * tempo) / float(60.0 * system_fps)
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
white_color = (200, 255, 200)
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((window_size["width"], window_size["height"]))
pygame.display.set_caption(title)
# font settings
font = pygame.font.SysFont(None, 20)

# bar image load
time_bar_image = pygame.image.load("images/bar.png").convert()
time_bar = time_bar_image.get_rect()
# bak image load
bak_image = pygame.image.load("images/bak.png").convert()
bak_bar = bak_image.get_rect()
# drum memories
_jsonPath = "./projects/" + project_name + "/breaks/meta.json"
with open(_jsonPath, encoding="utf-8", mode="r") as f:
    import json

    d = json.load(f)
# load sounds
break_list = []

for json in d:
    break_list.append("./projects/" + project_name + "/breaks/" + json["data"])

# ambient memories
_jsonPath = "./projects/" + project_name + "/ambient/meta.json"
with open(_jsonPath, encoding="utf-8", mode="r") as f:
    import json

    d = json.load(f)
# load sounds
sample1_list = [" * "]
sample1_json = [" * "]
sample2_list = [" * "]
sample2_json = [" * "]
for json in d:
    if json["sample1"] == True:
        sample1_list.append("./projects/" + project_name + "/ambient/" + json["data"])
        sample1_json.append(json["data"])
    else:
        sample2_list.append("./projects/" + project_name + "/ambient/" + json["data"])
        sample2_json.append(json["data"])


class SoundSquare:
    def __init__(self, audio_file, x_pos, y_pos, track_num):
        self.sizex = blockSizex
        self.sizey = blockSizey
        self.off = pygame.image.load("images/off.png").convert_alpha()
        self.on = pygame.image.load("images/on.png").convert_alpha()
        self.off_selected = pygame.image.load("images/off_selected.png").convert_alpha()
        self.on_selected = pygame.image.load("images/on_selected.png").convert_alpha()
        self._state = False
        self.rect = pygame.Rect(x_pos, y_pos, self.sizex, self.sizey)
        self.sound = pygame.mixer.Sound(audio_file)
        from pydub import AudioSegment
        _sound = AudioSegment.from_file(audio_file, "wav")
        _hoge = AudioSegment(
                    data=_sound._data,
                    sample_width=4, 
                    frame_rate=44100, 
                    channels=2,
        )
        _hoge = _hoge.reverse()
        self.reverse_sound = pygame.mixer.Sound(_hoge._data)

        _sound = AudioSegment.from_file(audio_file, "wav")
        _hoge = AudioSegment(
                    data=_sound._data,
                    sample_width=4, 
                    frame_rate=44100, 
                    channels=2,
        )
        _hoge = _hoge + _hoge
        self.twin_sound = pygame.mixer.Sound(_hoge._data)

    def get_state(self):
        return self._state

    def toggle_state(self):
        self._state = not self._state

    def render(self, isSelected):
        if self._state is False:
            if isSelected:
                window_surface.blit(self.off_selected, self.rect)
            else:
                window_surface.blit(self.off, self.rect)
        else:
            if isSelected:
                window_surface.blit(self.on_selected, self.rect)
            else:
                window_surface.blit(self.on, self.rect)


def change_state(sound_square):
    mouse_pos = pygame.mouse.get_pos()
    if sound_square.rect.collidepoint(mouse_pos):
        sound_square.toggle_state()


# Text rendering
def render_text(
    selected_mode, selected_sample1, selected_sample2, mod_list, mod_select
):
    x = (blockSizex) / 2
    y = (blockSizey) / 2

    # main picture
    y += float(window_size["height"]) * 2 / float(len(break_list) + 6)

    # mod
    if selected_mode == 0:
        render_text = font.render(
            "*(mod:     " + mod_list[mod_select] + ")", True, white_color
        )
    else:
        render_text = font.render(
            "mod:     " + mod_list[mod_select] + "", True, white_color
        )
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)
    y += float(window_size["height"]) / float(len(break_list) + 6)

    for i in range(len(break_list)):
        if selected_mode == 1 + i:
            render_text = font.render("*(bre" + str(i + 1) + ")", True, white_color)
        else:
            render_text = font.render("bre" + str(i + 1), True, white_color)
        render_text_rect = render_text.get_rect(center=(x, y))
        window_surface.blit(render_text, render_text_rect)
        y += float(window_size["height"]) / float(len(break_list) + 6)
    # s1
    if selected_mode == 9:
        render_text = font.render("*(sam1:     " +  sample1_json[selected_sample1] + ")", True, white_color)
    else:
        render_text = font.render("sam1:     " +  sample1_json[selected_sample1], True, white_color)
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)
    y += float(window_size["height"]) / float(len(break_list) + 6)

    # s2
    if selected_mode == 10:
        render_text = font.render("*(sam2:     " +  sample2_json[selected_sample2] + ")", True, white_color)
    else:
        render_text = font.render("sam2:     " +  sample2_json[selected_sample2], True, white_color)
    render_text_rect = render_text.get_rect(topleft=(x, y))
    window_surface.blit(render_text, render_text_rect)


def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()


# Check for collision between time bar and 'on' sound square
def collide(time_bar, track_list, mod_select):
    for track in track_list:
        for sound_square in track:
            if (
                time_bar.right >= sound_square.rect.left - s_tempo / 2
                and time_bar.right < sound_square.rect.left + s_tempo / 2
            ):
                if sound_square._state == True:
                    if mod_select == 2:
                        sound_square.reverse_sound.play()
                    elif mod_select == 3:
                        sound_square.twin_sound.play()
                    else:
                        sound_square.sound.play()
                    


# set up sound squares
track_list = []
for j in range(len(break_list)):
    track_list.append([])
    for i in range(0, sequence_number):
        sound_square = SoundSquare(
            break_list[j], blockSizex * (i + 1), blockSizey * (j + 3), j
        )
        track_list[j].append(sound_square)

# set up ambients
selected_sample1 = 1
selected_sample2 = 0
sample1_data = []
sample2_data = []
for j in range(len(sample1_list)):
    if sample1_list[j] != ' * ':
        sound_square = pygame.mixer.Sound(sample1_list[j])
    sample1_data.append(sound_square)
for j in range(len(sample2_list)):
    if sample2_list[j] != ' * ':
        sound_square = pygame.mixer.Sound(sample2_list[j])
    sample2_data.append(sound_square)

time_bar.right = blockSizex
time_bar.top = blockSizey * 3

mod_select = 1
mod_list = [" * ", "break select", "reverse", "twins"]

where_half = 0  # 0 -> 8 -> 16

selected_mode = 0  # x
selected_seq = 1  # y

seq_tempo = 0

# play only sample
if selected_sample1 != 0:
    sample1_data[selected_sample1].play()
if selected_sample2 != 0:
    sample2_data[selected_sample2].play()

while True:
    dt = main_clock.tick(float(system_fps))
    # on_list = []

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                selected_mode -= 1
                selected_mode = max(0, selected_mode)
                # temporary
                if selected_mode == 0:
                    seq_tempo = selected_seq
                    selected_seq = mod_select
                if selected_mode == 8:
                    selected_seq = seq_tempo
            if event.key == K_DOWN:
                selected_mode += 1
                selected_mode = min(10, selected_mode)
                # temporary
                if selected_mode == 9:
                    seq_tempo = selected_seq
                    selected_seq = selected_sample1
                if selected_mode == 10:
                    selected_seq = selected_sample2
                if selected_mode == 1:
                    mod_select = selected_seq
                    selected_seq = seq_tempo
            if event.key == K_LEFT:
                selected_seq -= 1
                if selected_mode == 0:
                    selected_seq = max(0, selected_seq)
                    mod_select = selected_seq
                elif selected_mode == 9:
                    selected_seq = max(0, selected_seq)
                    selected_sample1 = selected_seq
                elif selected_mode == 10:
                    selected_seq = max(0, selected_seq)
                    selected_sample2 = selected_seq
                else:
                    selected_seq = max(0, selected_seq)
            if event.key == K_RIGHT:
                selected_seq += 1
                if selected_mode == 0:
                    selected_seq = min(len(mod_list) -1, selected_seq)
                    mod_select = selected_seq
                elif selected_mode == 9:
                    selected_seq = min(len(sample1_data) -1, selected_seq)
                    selected_sample1 = selected_seq
                elif selected_mode == 10:
                    selected_seq = min(len(sample2_data) -1, selected_seq)
                    selected_sample2 = selected_seq
                else:
                    selected_seq = min(sequence_number -1, selected_seq)

            if event.key == K_SPACE:
                if selected_mode != 0 and selected_mode != 9 and selected_mode != 10:
                    track_list[selected_mode-1][selected_seq].toggle_state()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for track in track_list:
                for sound_square in track:
                    change_state(sound_square)

    if float(time_bar.right) > float(window_size["width"]) - float(s_tempo) - 1.0:
        time_bar.right = float(blockSizex) - s_tempo
        where_half += 8

        if where_half & 8 == 0:
            if selected_sample1 != 0:
                sample1_data[selected_sample1].play()
            if selected_sample2 != 0:
                sample2_data[selected_sample2].play()

    if main_clock.get_fps() > 30:
        time_bar.move_ip(float(s_tempo) * (float(main_clock.get_fps()) /  system_fps), 0)
    else:
        time_bar.move_ip(float(s_tempo), 0)

    window_surface.fill(black_color)

    for i, track in enumerate(track_list):
        for j, sound_square in enumerate(track):
            if i == selected_mode - 1 and j == selected_seq:
                sound_square.render(True)
            else:
                sound_square.render(False)

    render_text(selected_mode, selected_sample1, selected_sample2, mod_list, mod_select)
    if mod_select != 0:
        collide(time_bar, track_list, mod_select)

    window_surface.blit(time_bar_image, time_bar)
    window_surface.blit(bak_image, bak_bar)

    pygame.display.update()
