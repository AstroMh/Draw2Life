import time
from dataclasses import dataclass
from math import hypot
from typing import Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np


@dataclass
class HandMouseEvent:
    cursor_xy: Optional[Tuple[int, int]]
    click_down: bool
    hand_present: bool
    action: Optional[str] = None


class HoldTrigger:
    """Triggers once when condition stays True for hold_ms, then one-shot until released."""
    def __init__(self, hold_ms: int):
        self.hold_ms = hold_ms
        self._start_ms = None
        self._triggered = False

    def update(self, cond: bool) -> bool:
        now = int(time.time() * 1000)

        if not cond:
            self._start_ms = None
            self._triggered = False
            return False

        if self._start_ms is None:
            self._start_ms = now
            self._triggered = False
            return False

        if (not self._triggered) and (now - self._start_ms >= self.hold_ms):
            self._triggered = True
            return True

        return False


class VirtualHandMouse:
    def __init__(
        self,
        camera_index: int = 0,
        frame_size: Tuple[int, int] = (640, 480),
        smoothing: float = 0.35,
        mirror: bool = True,
        draw_landmarks: bool = True,
        backend: str = "auto",  # "auto" | "dshow" | "msmf"

        pinch_down_thresh: float = 30.0,
        pinch_up_thresh: float = 70.0,

        pointer_grace_ms: int = 350,

        clear_hold_ms: int = 900,

        max_hands: int = 1,
        detection_conf: float = 0.7,
        tracking_conf: float = 0.7,
        model_complexity: int = 0,
    ):
        cv2.setUseOptimized(True)

        self.frame_w, self.frame_h = frame_size
        self.smoothing = float(np.clip(smoothing, 0.0, 1.0))
        self.mirror = mirror
        self.draw_landmarks = draw_landmarks

        self.pinch_down_thresh = pinch_down_thresh
        self.pinch_up_thresh = pinch_up_thresh
        self.pointer_grace_ms = pointer_grace_ms

        self._prev_x = None
        self._prev_y = None
        self._click_state = False

        self._last_good_cursor = None
        self._last_good_cursor_ms = 0

        self._clear_hold = HoldTrigger(clear_hold_ms)

        self._last_time = time.time()
        self._fps = 0.0

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )

        api = 0
        if backend.lower() == "dshow":
            api = cv2.CAP_DSHOW
        elif backend.lower() == "msmf":
            api = cv2.CAP_MSMF

        self.cap = cv2.VideoCapture(camera_index, api) if api else cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open webcam at index {camera_index}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_h)

        for _ in range(10):
            ok, _ = self.cap.read()
            if ok:
                break

    def close(self):
        try:
            self.hands.close()
        except Exception:
            pass
        if self.cap is not None:
            self.cap.release()

    def read(self):
        ok, frame = self.cap.read()
        if not ok:
            return False, None
        return True, frame

    def _update_fps(self):
        now = time.time()
        dt = now - self._last_time
        self._last_time = now
        if dt > 0:
            inst = 1.0 / dt
            self._fps = 0.9 * self._fps + 0.1 * inst

    def _smooth_xy(self, x: float, y: float) -> Tuple[int, int]:
        if self._prev_x is None or self._prev_y is None:
            self._prev_x, self._prev_y = x, y
        else:
            self._prev_x = self._prev_x + (x - self._prev_x) * self.smoothing
            self._prev_y = self._prev_y + (y - self._prev_y) * self.smoothing
        return int(self._prev_x), int(self._prev_y)

    @staticmethod
    def _finger_extended(lm, tip: int, pip: int, margin: float = 0.02) -> bool:
        return (lm[tip].y + margin) < lm[pip].y

    def process_frame(self, frame_bgr):
        if self.mirror:
            frame_bgr = cv2.flip(frame_bgr, 1)

        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        hand_present = bool(results.multi_hand_landmarks)
        cursor_xy = None
        action = None

        now_ms = int(time.time() * 1000)

        if hand_present:
            hand_landmarks = results.multi_hand_landmarks[0]
            lm = hand_landmarks.landmark

            def px(idx):
                return int(lm[idx].x * w), int(lm[idx].y * h)

            x_thumb, y_thumb = px(4)
            x_middle, y_middle = px(12)

            cursor_xy = self._smooth_xy(x_thumb, y_thumb)
            self._last_good_cursor = cursor_xy
            self._last_good_cursor_ms = now_ms

            # Drawing: thumb-middle pinch with hysteresis
            dist_tm = hypot(x_middle - x_thumb, y_middle - y_thumb)
            if dist_tm <= self.pinch_down_thresh:
                self._click_state = True
            elif dist_tm >= self.pinch_up_thresh:
                self._click_state = False

            # Clear gesture: OPEN PALM held
            index_ext = self._finger_extended(lm, 8, 6)
            middle_ext = self._finger_extended(lm, 12, 10)
            ring_ext = self._finger_extended(lm, 16, 14)
            pinky_ext = self._finger_extended(lm, 20, 18)
            open_palm = index_ext and middle_ext and ring_ext and pinky_ext

            if not self._click_state:
                if self._clear_hold.update(open_palm):
                    action = "CLEAR"
            else:
                self._clear_hold.update(False)

            if self.draw_landmarks:
                self.mp_draw.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(thickness=2, circle_radius=2),
                    self.mp_draw.DrawingSpec(thickness=2, circle_radius=2),
                )
                cx, cy = cursor_xy
                cv2.circle(frame_bgr, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

        else:
            if self._last_good_cursor is not None and (now_ms - self._last_good_cursor_ms <= self.pointer_grace_ms):
                cursor_xy = self._last_good_cursor
            else:
                self._last_good_cursor = None
                cursor_xy = None

            self._click_state = False
            self._clear_hold.update(False)
            action = None

        self._update_fps()
        cv2.putText(frame_bgr, f"FPS: {self._fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if action:
            cv2.putText(frame_bgr, f"ACTION: {action}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        return frame_bgr, HandMouseEvent(
            cursor_xy=cursor_xy,
            click_down=self._click_state,
            hand_present=hand_present,
            action=action
        )
