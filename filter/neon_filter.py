import cv2
import numpy as np
from queue import Queue

class NeonFilter:
    def __init__(self, outputs=None):
        self.outputs = outputs or []
        self.input = Queue()

    def process(self):
        while True:
            frame = self.input.get()
            if frame is None:
                break
            # Increase the brightness and add a neon color map
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv[..., 2] = np.minimum(hsv[..., 2] * 2, 255)  # Brighten the image
            bright_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            neon_frame = cv2.applyColorMap(bright_frame, cv2.COLORMAP_JET)

            # Pass to outputs
            for output in self.outputs:
                output.put(neon_frame)
