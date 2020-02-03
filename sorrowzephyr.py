"""
Copyright 2020, Keith Kotyk, Adam Lozinsky All rights reserved.
"""
import urwid
import subprocess as sp
import threading
import signal
import os
import json

import PIL.Image
import aalib
import sys

title_full = """
                                       ▄▄▄▄▀ ▄  █ ▄███▄       ▄███▄   █     ██▄   ▄███▄   █▄▄▄▄        ▄▄▄▄▄   ██     ▄▀  ██
                                    ▀▀▀ █   █   █ █▀   ▀      █▀   ▀  █     █  █  █▀   ▀  █  ▄▀       █     ▀▄ █ █  ▄▀    █ █
                                        █   ██▀▀█ ██▄▄        ██▄▄    █     █   █ ██▄▄    █▀▀▌      ▄  ▀▀▀▀▄   █▄▄█ █ ▀▄  █▄▄█
                                       █    █   █ █▄   ▄▀     █▄   ▄▀ ███▄  █  █  █▄   ▄▀ █  █       ▀▄▄▄▄▀    █  █ █   █ █  █
                                      ▀        █  ▀███▀       ▀███▀       ▀ ███▀  ▀███▀     █                     █  ███     █
                                              ▀                                            ▀                     █          █
                                                                                                                ▀          ▀


           ▄████████  ▄██████▄     ▄████████    ▄████████  ▄██████▄   ▄█     █▄   ▄███████▄  ▄██   ▄      ▄███████▄    ▄█    █▄       ▄████████    ▄████████
          ███    ███ ███    ███   ███    ███   ███    ███ ███    ███ ███     ███ ██▀     ▄██ ███   ██▄   ███    ███   ███    ███     ███    ███   ███    ███
          ███    █▀  ███    ███   ███    ███   ███    ███ ███    ███ ███     ███       ▄███▀ ███▄▄▄███   ███    ███   ███    ███     ███    █▀    ███    ███
          ███        ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄▄██▀ ███    ███ ███     ███  ▀█▀▄███▀▄▄ ▀▀▀▀▀▀███   ███    ███  ▄███▄▄▄▄███▄▄  ▄███▄▄▄      ▄███▄▄▄▄██▀
        ▀███████████ ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀▀▀   ███    ███ ███     ███   ▄███▀   ▀ ▄██   ███ ▀█████████▀  ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀
                 ███ ███    ███ ▀███████████ ▀███████████ ███    ███ ███     ███ ▄███▀       ███   ███   ███          ███    ███     ███    █▄  ▀███████████
           ▄█    ███ ███    ███   ███    ███   ███    ███ ███    ███ ███ ▄█▄ ███ ███▄     ▄█ ███   ███   ███          ███    ███     ███    ███   ███    ███
         ▄████████▀   ▀██████▀    ███    ███   ███    ███  ▀██████▀   ▀███▀███▀   ▀████████▀  ▀█████▀   ▄████▀        ███    █▀      ██████████   ███    ███
                                  ███    ███   ███    ███                                                                                         ███    ███



 ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄   ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄     ▄▀▀▀▀▄   ▄▀▀▀█▄       ▄▀▀▀█▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄▄▄▄     ▄▀▀▀█▄    ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄  ▄▀▀█▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▄
█   █   █ █   █  █ █ █   ▐ ▐  ▄▀   ▐    █      █ █  ▄▀  ▀▄    █    █  ▐ █  █   ▄▀ ▐  ▄▀   ▐    █  ▄▀  ▀▄ █      █ █   █   █ █ █   ▐ ▐ ▄▀ ▀▄ █  █ ▄▀ ▐  ▄▀   ▐ █  █ █ █
▐  █▀▀█▀  ▐   █  ▐    ▀▄     █▄▄▄▄▄     █      █ ▐ █▄▄▄▄      ▐   █     ▐  █▄▄▄█    █▄▄▄▄▄     ▐ █▄▄▄▄   █      █ ▐  █▀▀█▀     ▀▄     █▄▄▄█ ▐  █▀▄    █▄▄▄▄▄  ▐  █  ▀█
 ▄▀    █      █    ▀▄   █    █    ▌     ▀▄    ▄▀  █    ▐         █         █   █    █    ▌      █    ▐   ▀▄    ▄▀  ▄▀    █  ▀▄   █   ▄▀   █   █   █   █    ▌    █   █
█     █    ▄▀▀▀▀▀▄  █▀▀▀    ▄▀▄▄▄▄        ▀▀▀▀    █            ▄▀         ▄▀  ▄▀   ▄▀▄▄▄▄       █          ▀▀▀▀   █     █    █▀▀▀   █   ▄▀  ▄▀   █   ▄▀▄▄▄▄   ▄▀   █
▐     ▐   █       █ ▐       █    ▐               █            █          █   █     █    ▐      █                  ▐     ▐    ▐      ▐   ▐   █    ▐   █    ▐   █    ▐
          ▐       ▐         ▐                    ▐            ▐          ▐   ▐     ▐           ▐                                            ▐        ▐        ▐


             _     _     __   _______    _______ _____ ______    ________     _______    _  _  _____      ______     _  _  ___________________     _
             |_____|     | \  |  |       |______|     |_____/       |   |_____|______    |  |  | |  |     |     \    |  |  | |    |   |      |_____|
             |     |_____|  \_|  |       |      |_____|    \_       |   |     |______    |__|__|_|__|_____|_____/    |__|__|_|__  |   |_____ |     |


                                        ▄▄▄ . ▐ ▄ ·▄▄▄▄▄▌   ▄▄▄· • ▌ ▄ ·. ▄▄▄ .·▄▄▄▄       ▐▄▄▄▪   ▄ .▄ ▄▄▄· ·▄▄▄▄
                                        ▀▄.▀·•█▌▐█▐▄▄·██•  ▐█ ▀█ ·██ ▐███▪▀▄.▀·██▪ ██       ·████ ██▪▐█▐█ ▀█ ██▪ ██
                                        ▐▀▀▪▄▐█▐▐▌██▪ ██▪  ▄█▀▀█ ▐█ ▌▐▌▐█·▐▀▀▪▄▐█· ▐█▌    ▪▄ ██▐█·██▀▐█▄█▀▀█ ▐█· ▐█▌
                                        ▐█▄▄▌██▐█▌██▌.▐█▌▐▌▐█ ▪▐▌██ ██▌▐█▌▐█▄▄▌██. ██     ▐▌▐█▌▐█▌██▌▐▀▐█ ▪▐▌██. ██
                                         ▀▀▀ ▀▀ █▪▀▀▀ .▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀ ▀▀▀ ▀▀▀▀▀•      ▀▀▀•▀▀▀▀▀▀ · ▀  ▀ ▀▀▀▀▀•


"""

class PileOverride(urwid.Pile):
    def mouse_event(self, size, event, button, col, row, focus):
        pass

class GameHandler():
    def __init__(self):
        self.animations = []
        self.ani_state = 0

        self.music = True
        self.tts = True

        self.speak_flag = False

        self.all_frames = {}
        self.inventory = []

        self.current_song = 'Hemispheres.mp3'
        self.create_game_content()

        self.columns_box = urwid.Columns([urwid.Text("Anguis et Corvis\nProductions", align='center')])
        fill = urwid.Filler(self.columns_box,'top')

        self.loop = urwid.MainLoop(fill, unhandled_input=self.handle_keys)

        self.loop.set_alarm_in(2, self.switch_to_title)
        self.loop.run()

    def update_box(self, widget, state, option_data):

        cmd = "killall espeak"
        sp.call(cmd, shell=True)

        if option_data['frame'] == -1:
            sys.exit(1)

        new_frame = self.all_frames[option_data['frame']]

        if new_frame['frame_num'] == 33 and 'nailsQuest' in self.inventory and 'shovelQuest' in self.inventory:
            self.inventory.remove('shovelQuest')
            self.inventory.remove('nailsQuest')

        dialog_text = new_frame['dialog']
        self.dialog_box.set_text(dialog_text)

        button_options = self.choice_box.options()
        buttons = []

        debug_txt = str(new_frame['frame_num'])+"\n"+repr(self.inventory) + "\n"

        skip_opt = False
        for opt in new_frame['options']:
            debug_txt += repr(opt['flags']) + "\n"
            for flag in opt['flags']:
                if flag not in self.inventory:
                    skip_opt = True
            if skip_opt:
                skip_opt = False
                continue

            new_button = urwid.CheckBox(opt['opt'],
                                        state=False,
                                        on_state_change=self.update_box,
                                        user_data=opt)

            buttons.append((new_button, button_options))

        self.inventory.extend(option_data['sets'])

        self.debug_box.set_text(debug_txt)
        self.choice_box.contents = buttons

        self.animations = new_frame['animations']
        self.ani_state = 0
        self.death_frame = False

        if new_frame['frame_num'] in [0,12,13,14,17,26,27,28,44,45,49,56,57,59,60,61]:
            song = 'Hemispheres.mp3'
        elif new_frame['frame_num'] in [38,39,40,41,43,58]:
            song = 'sadriver.mp3'
        else:
            song = 'town.mp3'

        if self.music and self.current_song != song:
            self.current_song = song
            self.stop_music()

        if new_frame['speak_frame'] is True and self.tts:
            speak_thread = threading.Thread(target=self.lets_speak_callback, args=(dialog_text, ))
            speak_thread.daemon = True
            speak_thread.start()
            new_frame['speak_frame'] = False

    def handle_keys(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def main_loop_callback(self, main_loop, data):

        self.art_box.set_text(self.animations[self.ani_state])
        self.ani_state = (self.ani_state + 1) % len(self.animations)

        main_loop.set_alarm_in(0.1, self.main_loop_callback)

    def switch_to_title(self, main_loop, data):
        self.columns_box.focus.set_align_mode('left')
        self.columns_box.focus.set_text(title_full)
        main_loop.set_alarm_in(2, self.switch_to_game)

    def switch_to_game(self, main_loop, data):
        self.art_box = urwid.Text("")

        start_text = ("Welcome to The Elder Saga: Sorrowzypher, Rise of the Forsaken, Hunt of the Wild Witch, The Enflamed Jihad!\n\n"
                     "The world is in great need of a hero and savior! Someone like.....well, someone not like you.\n\n\n\n\n\n\n\n"
                      "Use the arrow keys to navagate options. Press enter to confirm your choice.")
        self.dialog_box = urwid.Text(start_text, align='center')

        opt_data = {"opt" : "Start your adventure!",
                      "frame" : 0,
                      "flags" : [],
                      "sets" : []}
        d_music = {"opt" : "Disable music.",
                      "frame" : 0,
                      "flags" : [],
                      "sets" : []}
        d_tts = {"opt" : "Disable narration.",
                      "frame" : 0,
                      "flags" : [],
                      "sets" : []}
        start_adventure = urwid.CheckBox(opt_data['opt'], state=False,
                            on_state_change=self.update_box, user_data=opt_data)
        disable_music = urwid.CheckBox(d_music['opt'], state=False,
                            on_state_change=self.toggle_music, user_data=d_music)
        disable_tts = urwid.CheckBox(d_tts['opt'], state=False,
                            on_state_change=self.toggle_tts, user_data=d_tts)

        self.choice_box = PileOverride([start_adventure,disable_music,disable_tts])
        padded_c_box = urwid.Padding(self.choice_box, align='right', width='pack')

        self.debug_box = urwid.Text("")


        piles = [urwid.LineBox(box) for box in [self.dialog_box, padded_c_box]]
        pile_box = urwid.Pile(piles)

        columns_options = self.columns_box.options()
        self.columns_box.contents = [(urwid.LineBox(pile_box), columns_options),
                                        (urwid.LineBox(self.art_box), columns_options)]

        self.loop.set_alarm_in(0.05, self.main_loop_callback)

        self.music_thread = threading.Thread(target=self.start_music)
        self.music_thread.daemon = True
        self.music_thread.start()

    def lets_speak_callback(self, words):
        speak_cmd = 'espeak -s195 -k7 "{}" 2>>/dev/null'.format(words)
        p = sp.Popen(speak_cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        output, err = p.communicate()

    def stop_music(self):
        cmd = "killall mplayer"
        sp.call(cmd, shell=True)

    def start_music(self):
        music_cmd = 'mplayer -volume 50 {} 2>>/dev/null'
        while True and self.music:
            cmd = music_cmd.format(self.current_song)
            p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            output, err = p.communicate()

    def toggle_music(self, widget, state, option_data):
        old_val = self.music
        self.music = not self.music
        if old_val:
            self.stop_music()
        else:
            self.start_music()



    def toggle_tts(self, widget, state, option_data):
        self.tts = not self.tts

    def create_game_content(self):
        frame_dir = "GamesJam"

        for d in os.listdir(frame_dir):
            if "frame" in d and not "json" in d:
                a = d.split("_")
                with open(frame_dir+"/"+d+"/"+d+".json") as f:
                    json_data = json.load(f)
                    self.all_frames[int(a[1])] = json_data

                self.all_frames[int(a[1])]['speak_frame'] = True
                self.all_frames[int(a[1])]['animations'] = []

                all_files = os.listdir(frame_dir+"/"+d+"/animations")
                txts = [x for x in all_files if '.txt' in x]
                txts = sorted(txts)
                for txt in txts:
                    with open(frame_dir+"/"+d+"/animations/"+txt, 'r') as f:
                        self.all_frames[int(a[1])]['animations'].append(f.read())

            if "intro" in d:
                all_files = os.listdir(frame_dir+"/"+d+"/animations")
                txts = [x for x in all_files if '.txt' in x]
                txts = sorted(txts)
                for txt in txts:
                    with open(frame_dir+"/"+d+"/animations/"+txt, 'r') as f:
                        self.animations.append(f.read())

GameHandler()

