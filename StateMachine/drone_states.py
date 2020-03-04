from StateMachine.State import State


class IdleState (State):
    def on_event(self, event):
        if (event == 'take_off'):
            return TakeOffState()
        return self

class TakeOffState (State):
    def on_event(self, event):
        if (event == 'track'):
            return TrackState()
        elif (event == "land"):
            return LandState()
        return self

class TrackState (State):
    def on_event(self, event):
        if (event == "land"):
            return LandState()
        return self

class LandState (State):
    def on_event(self, event):
        if (event == "idle"):
            return IdleState()
        return self

