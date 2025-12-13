import cv2

from src.gesture_detection import VirtualHandMouse
from src.game_of_life_gui import GameOfLifeGUI


class HandControlledLifeApp:
    def __init__(self, life: GameOfLifeGUI, hand: VirtualHandMouse, poll_ms: int = 10, show_camera: bool = True):
        self.life = life
        self.hand = hand
        self.poll_ms = poll_ms
        self.show_camera = show_camera

        self.canvas_w = self.life.cols * self.life.cell_size
        self.canvas_h = self.life.rows * self.life.cell_size

        self.pinch_confirm_frames = 3
        self.pinch_release_frames = 2
        self._pinch_on = 0
        self._pinch_off = 0
        self._drawing_active = False

        self._last_draw_cell = None

        self.life.root.after(1, self.poll_camera)
        self.life.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.cleanup()
        self.life.root.destroy()

    def cleanup(self):
        try:
            self.hand.close()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

    def _update_drawing_state(self, pinch_now: bool):
        if pinch_now:
            self._pinch_on += 1
            self._pinch_off = 0
        else:
            self._pinch_off += 1
            self._pinch_on = 0

        if (not self._drawing_active) and (self._pinch_on >= self.pinch_confirm_frames):
            self._drawing_active = True
            self._last_draw_cell = None
        elif self._drawing_active and (self._pinch_off >= self.pinch_release_frames):
            self._drawing_active = False
            self._last_draw_cell = None

    def poll_camera(self):
        ok, frame = self.hand.read()
        if ok and frame is not None:
            annotated, event = self.hand.process_frame(frame)

            if self.show_camera:
                cv2.imshow("Hand Tracker Preview (press q to hide)", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.show_camera = False
                    cv2.destroyAllWindows()

            fh, fw = frame.shape[:2]

            if event.action == "CLEAR":
                self.life.clear_grid()

            self._update_drawing_state(event.click_down)

            draw_mode = (self.life.mode_var.get() == "Draw")

            if event.cursor_xy is not None:
                x_f, y_f = event.cursor_xy
                x_f = max(0, min(fw - 1, x_f))
                y_f = max(0, min(fh - 1, y_f))

                x_c = int(x_f * self.canvas_w / fw)
                y_c = int(y_f * self.canvas_h / fh)

                col = x_c // self.life.cell_size
                row = y_c // self.life.cell_size

                self.life.highlight_cell(row, col)

                if draw_mode and self._drawing_active:
                    cell = (row, col)
                    if cell != self._last_draw_cell:
                        self.life.set_cell(row, col, True)
                        self.life.draw_grid()
                        self._last_draw_cell = cell
            else:
                self.life.highlight_cell(-1, -1)

        self.life.root.after(self.poll_ms, self.poll_camera)


if __name__ == "__main__":
    life = GameOfLifeGUI(rows=30, cols=50, cell_size=20, delay=120)

    hand = VirtualHandMouse(
        camera_index=1,
        frame_size=(640, 480),
        smoothing=0.35,
        mirror=True,
        draw_landmarks=True,
        backend="auto",
        pinch_down_thresh=30.0,
        pinch_up_thresh=70.0,
        pointer_grace_ms=350,
        clear_hold_ms=900,
        max_hands=1,
        model_complexity=0,
    )

    controller = HandControlledLifeApp(life, hand, poll_ms=10, show_camera=True)

    try:
        life.run()
    finally:
        controller.cleanup()
