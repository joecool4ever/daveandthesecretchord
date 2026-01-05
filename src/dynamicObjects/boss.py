from .dynamicObject import DynamicObject, ObjectStates
from animationsystem import AnimationController, Animation
from objectTypes import GameObjectTypes

class Boss(DynamicObject):
    def __init__(self, pos, name, type, width, height, game, *groups, health = 100, cor = True):
        self.x, self.y = pos
        super().__init__(self.x, self.y, name, *groups, type = type, width=width, height=height, game = game)

        self.cor = True

        # self.cor_idle_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE, type = "object"), 15, extra_anim=self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE_BLINK, type="object"), rev_loop = True)
        # self.cor_idle_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.IDLE, type = "object"), 15, rev_loop = False)
        # self.cor_run_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.RUNNING, type = "object"), 5)
        # self.cor_jump_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.JUMPING, type = "object"), 10)
        # self.cor_fall_animation = Animation(self.assets.load_images(self.name + "_cor", state = ObjectStates.FALLING, type = "object"), 10)