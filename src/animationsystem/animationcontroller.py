import pygame
import random
from enums import ObjectStates, Instruments
from .animation import Animation
from rects import *

class AnimationController():
    def __init__(self, type, name = "", rev_loop = False, extra_anim = None, anims_needed = [], instruments = [], assets = None):
        
        #animation rate variables
        self.extra_anim = extra_anim
        self.frame_counter = 0

        #current frame
        self.animation_frames = {}

        # How long to Blink
        self.blink_timer = 0

        #animation loading
        self.name = name
        self.anims_needed = anims_needed
        self.instruments = instruments
        self.owned_anims = {}
        self.assets = assets

        self.current_anim = None

        self.load_frames(type, name, anims_needed, instruments)


    def load_subsurf(self, list_of_rects, name, subname="", type = ""):
        key = name + subname
        subsurfs = []
        for rect in list_of_rects:
            if key in self.assets.sprite_sheets:
                sprite_sheet = self.assets.sprite_sheets[key]
                if type in scales:
                    
                    subsurfs.append(pygame.transform.scale(sprite_sheet.subsurface(rect), (rect.width * scales[type], rect.height * scales[type])))
                else:
                    subsurfs.append(pygame.transform.scale(sprite_sheet.subsurface(rect), (rect.width * 1, rect.height * 1)))
            else:
                print(f"{key} not in sprite_sheets")
            
        return subsurfs
    
    def load_frames(self, type, name, anims_needed, instruments = []):
        subname = ""
        if type == "object":
            for anim in anims_needed:
                if anim in move_animation_rects:
                    print(f"Adding {anim} to Animations")

                    rects = move_animation_rects[anim][0]
                    subsurfs = self.load_subsurf(rects, self.name, subname=subname)
                    if anim == ObjectStates.SLIDING:
                        subsurfs[0] = pygame.transform.flip(subsurfs[0], True, False)

                    self.owned_anims[anim] = Animation(anim, subsurfs, move_animation_rects[anim][1])
                else:
                    print(f'Anim name: {anim} not in Keys')
            for instrument in instruments:
                if instrument in attack_animation_rects:
                    rects = attack_animation_rects[instrument][0]
                    print(f'Instrument name: {instrument} added to Animations')
                    self.owned_anims[str(instrument)] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack"), attack_animation_rects[instrument][1])
                    self.owned_anims[str(instrument) + " walk"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_walk"), attack_animation_rects[instrument][1])

                    
                    if instrument in attack_jump_animation_rects:
                        rects = attack_jump_animation_rects[instrument][0]
                        self.owned_anims[str(instrument) + " jump"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_jump_animation_rects[instrument][1])
                    if instrument in attack_fall_animation_rects:
                        rects = attack_fall_animation_rects[instrument][0]
                        self.owned_anims[str(instrument) + " fall"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_fall_animation_rects[instrument][1])
                else:
                    print(f'Instrument name: {instrument} not in Keys')
        else:
            if "note" in name:
                self.owned_anims[name] = Animation(name, self.load_subsurf(notes_rects[name.removesuffix("note")], "items_test", subname = subname, type = "note"), 6)
            else:
                self.owned_anims[name] = Animation(name, self.load_subsurf(item_rects[name][0], "items_test", subname = subname, type = name), item_rects[name][1])

            

            
    def animate(self, dt, state = "health", instrument = None, reset = False):
        
        if state == ObjectStates.ATTACKING:
            state = str(instrument)
        elif state == ObjectStates.ATTACKING_WALK:
            state = str(instrument) + " walk"
        elif state == ObjectStates.ATTACKING_JUMP:
            state = str(instrument) + " jump"
        elif state == ObjectStates.ATTACKING_FALL:
            state = str(instrument) + " fall"
        if state in self.owned_anims:
            self.current_anim = state
            current_frames = self.owned_anims[state]

            if reset:
                self.animation_frame = 0
                self.frame_counter = 0
            
            if random.random() < 0.1 and self.extra_anim:
                self.blink_timer = .15
                return self.extra_anim[0]
            
            if self.blink_timer > 0 and self.extra_anim:
                self.blink_timer -= dt
                return self.extra_anim[0]
            index = 0
            try:
                index = self.grab_index(dt, state, current_frames)
                return current_frames.frames[index]
            except(IndexError):
                print(f"Erroring on {state} with index: {index}")
                return pygame.Surface((35,35))
        else:
            print(f"{state} not a animation applied to {self.name}")
            return pygame.Surface((35,35))
    
    def grab_index(self, dt, state_or_instrument, current_frames):

        frames = current_frames.frames
        frame_speed = current_frames.frame_speed

        if state_or_instrument not in self.animation_frames:
            self.animation_frames[state_or_instrument] = 0
        self.frame_counter += dt
        if self.frame_counter >= frame_speed / 60:
            self.extra_anim_placeholder = None
            # self.animation_frame = (self.animation_frame + 1) % len(self.full_animation)
            self.animation_frames[state_or_instrument] = (self.animation_frames[state_or_instrument] + 1) % len(frames)
            self.frame_counter -= frame_speed / 60  
        return self.animation_frames[state_or_instrument]
    
    def update_frame_rate(self, adjust):
        self.owned_anims[self.current_anim][1] += adjust
        print(f'{self.current_anim} set to {self.owned_anims[self.current_anim][1]}')
