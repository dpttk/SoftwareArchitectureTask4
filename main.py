import cv2
import threading
from queue import Queue
from filter import NeonFilter, VHSFilter, CyberpunkFilter, ResizeFilter

sink_pipe = Queue()

neon = NeonFilter(outputs=[])
vhs = VHSFilter(outputs=[neon.input, sink_pipe])
cyberpunk = CyberpunkFilter(outputs=[vhs.input])
resize = ResizeFilter(outputs=[cyberpunk.input])

source_pipe = resize.input


filters = [resize, cyberpunk, vhs, neon]
threads = []
for f in filters:
    t = threading.Thread(target=f.process)
    t.start()
    threads.append(t)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    source_pipe.put(frame)
    if not sink_pipe.empty():
        processed_frame = sink_pipe.get()
        cv2.imshow('Processed Webcam Feed', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

for queue in [source_pipe, resize.input, cyberpunk.input, vhs.input, neon.input]:
    queue.put(None)

for t in threads:
    t.join()
