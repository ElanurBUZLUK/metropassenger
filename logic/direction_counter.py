class DirectionCounter:
    def __init__(self, door_roi, entry_line_x, exit_line_x, cooldown_frames=45):
        self.door_roi = door_roi
        self.entry_line_x = entry_line_x
        self.exit_line_x = exit_line_x
        self.cooldown_frames = cooldown_frames
        self._initialize_state()

    def _initialize_state(self):
        self.previous_positions = {}
        self.track_states = {}
        self.cooldown_timers = {}
        self.binen_count = 0
        self.inen_count = 0

    def update(self, track):
        if not track.is_confirmed():
            track_id = track.track_id
            self.previous_positions.pop(track_id, None)
            self.track_states.pop(track_id, None)
            self.cooldown_timers.pop(track_id, None)
            return

        track_id = track.track_id
        x1, y1, x2, y2 = map(int, track.to_tlbr())
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        roi_x1, roi_y1, roi_x2, roi_y2 = self.door_roi

        if not (roi_x1 <= center_x <= roi_x2 and roi_y1 <= center_y <= roi_y2):
            if track_id in self.track_states and self.track_states[track_id] in ['counted_in', 'counted_out']:
                self.track_states[track_id] = 'initial'
            elif self.track_states.get(track_id) in ['crossing_in', 'crossing_out']:
                self.track_states[track_id] = 'initial'
            self.previous_positions[track_id] = center_x
            return

        if self.cooldown_timers.get(track_id, 0) > 0:
            self.cooldown_timers[track_id] -= 1
            self.previous_positions[track_id] = center_x
            return

        if track_id not in self.track_states:
            self.track_states[track_id] = 'initial'
            self.previous_positions[track_id] = center_x
            return

        prev_x = self.previous_positions[track_id]
        current_state = self.track_states[track_id]

        if current_state == 'initial' and prev_x < self.entry_line_x and center_x >= self.entry_line_x:
            self.track_states[track_id] = 'crossing_in'
        elif current_state == 'crossing_in' and prev_x < self.exit_line_x and center_x >= self.exit_line_x:
            self.binen_count += 1
            self.track_states[track_id] = 'counted_in'
            self.cooldown_timers[track_id] = self.cooldown_frames
        elif current_state == 'initial' and prev_x > self.exit_line_x and center_x <= self.exit_line_x:
            self.track_states[track_id] = 'crossing_out'
        elif current_state == 'crossing_out' and prev_x > self.entry_line_x and center_x <= self.entry_line_x:
            self.inen_count += 1
            self.track_states[track_id] = 'counted_out'
            self.cooldown_timers[track_id] = self.cooldown_frames
        elif current_state == 'crossing_in' and center_x < self.entry_line_x:
            self.track_states[track_id] = 'initial'
        elif current_state == 'crossing_out' and center_x > self.exit_line_x:
            self.track_states[track_id] = 'initial'

        self.previous_positions[track_id] = center_x

    def get_counts(self):
        return self.binen_count, self.inen_count

    def reset_counts(self):
        self._initialize_state()
