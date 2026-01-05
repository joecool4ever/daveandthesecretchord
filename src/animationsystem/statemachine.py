from enums import ObjectStates

class StateMachine():

    def stateChange(object, state, movement, freeze):
        if freeze:
            if abs(movement[0]) > 0.1:
                state = ObjectStates.RUNNING
            else:
                state = ObjectStates.IDLE

        else:   
            object.animation_stall = max(0, object.animation_stall - 1)
            if object.animation_stall == 0:
                if not object.crouching:
                    if object.grounded_timer > 0:
                        if abs(movement[0]) > 0.1:
                            state = ObjectStates.RUNNING
                        else:
                            state = ObjectStates.IDLE
                    else:
                        if object.vel[1] < 0:
                            state = ObjectStates.JUMPING
                        else:
                            if object.col['left'] or object.col['right']:
                                state = ObjectStates.SLIDING
                            else:
                                state = ObjectStates.FALLING
                else:
                    if object.grounded_timer > 0:
                        if abs(movement[0]) > 0.1:
                            state = ObjectStates.CROUCH_WALK
                        else:
                            state = ObjectStates.CROUCH_IDLE
                    else:
                        if object.vel[1] < 0:
                            state = ObjectStates.JUMPING
                        else:
                            state = ObjectStates.FALLING
            
                if object.dashing:
                    state = ObjectStates.DASHING
                    object.animation_stall = 5

                if object.attacking:
                    if object.grounded_timer > 0:
                        if abs(movement[0]) > 0.1:
                            state = ObjectStates.ATTACKING_WALK
                        else:
                            state = ObjectStates.ATTACKING

                    else:
                        if object.vel[1] < 0:
                            state = ObjectStates.ATTACKING_JUMP
                        else:
                            state = ObjectStates.ATTACKING_FALL
                
        return state
        