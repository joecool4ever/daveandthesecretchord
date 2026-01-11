from enum import Enum

class ObjectStates(Enum):
    IDLE = "Idle"
    RUNNING = "Running"
    JUMPING = "Jumping"
    FALLING = "Falling"
    IDLE_BLINK = "Idle Blink"
    CROUCH_IDLE = "Crouch Idle"
    CROUCH_WALK = "Crouch Walk"
    DASHING = "Dashing"
    ATTACKING = "Attacking"
    ATTACKING_WALK = "Attacking Walk"
    ATTACKING_JUMP = "Attacking Jump"
    ATTACKING_FALL = "Attacking Fall"
    SLIDING = "Sliding"

class Instruments(Enum):
    LYRE = "Lyre"
    MIC = "Mic"
    DRUMS = "Drums"
    BASS = "Bass"
    VIOLIN = "Violin"
    TRUMPET = "Trumpet"