import cv2
from queue import Queue

class ResizeFilter:
    def __init__(self, outputs=None):
        self.outputs = outputs or []
        self.input = Queue()

    def process(self):
        while True:
            frame = self.input.get()
            if frame is None:
                break
            # Resize the frame to 320x240
            resized_frame = cv2.resize(frame, (320, 240))

            # Pass to outputs
            for output in self.outputs:
                output.put(resized_frame)
