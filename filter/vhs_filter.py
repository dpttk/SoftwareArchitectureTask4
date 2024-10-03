import cv2
import numpy as np
from queue import Queue

class VHSFilter:
    def __init__(self, outputs=None):
        self.outputs = outputs or []
        self.input = Queue()

    def process(self):
        while True:
            frame = self.input.get()
            if frame is None:
                break
            # Create VHS glitch effect by shifting the frame and adding horizontal lines
            glitch_frame = frame.copy()

            # Random horizontal shift for glitch effect
            shift = np.random.randint(-5, 5)
            glitch_frame = np.roll(glitch_frame, shift, axis=1)

            # Add random horizontal lines for VHS noise
            for i in range(0, frame.shape[0], 10):
                if np.random.rand() > 0.8:
                    glitch_frame[i:i+2, :] = np.random.randint(0, 256, size=(2, frame.shape[1], 3))

            # Pass to outputs
            for output in self.outputs:
                output.put(glitch_frame)
