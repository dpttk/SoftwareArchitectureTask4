import cv2
import numpy as np
from queue import Queue

class CyberpunkFilter:
    def __init__(self, outputs=None):
        self.outputs = outputs or []
        self.input = Queue()

    def process(self):
        while True:
            frame = self.input.get()
            if frame is None:
                break
            # Add random pixel noise (cyberpunk style)
            noise = np.random.normal(0, 25, frame.shape).astype(np.uint8)
            noisy_frame = cv2.addWeighted(frame, 0.8, noise, 0.2, 0)

            # Pixelation effect by resizing down and back up
            small_frame = cv2.resize(noisy_frame, (64, 64), interpolation=cv2.INTER_LINEAR)
            pixel_frame = cv2.resize(small_frame, frame.shape[1::-1], interpolation=cv2.INTER_NEAREST)

            # Pass to outputs
            for output in self.outputs:
                output.put(pixel_frame)
