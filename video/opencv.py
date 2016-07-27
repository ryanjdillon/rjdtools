def play_video(video_path):
    '''Video playback'''
    import sys

    import cv2

    # http://web.michaelchughes.com/how-to/watch-video-in-python-with-opencv

    try:
        cap = cv2.VideoCapture(video_path)
    except:
        print("problem opening input stream")
        sys.exit(1)
    if not cap.isOpened():
        print("capture stream not open")
        sys.exit(1)

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_pause_ms = int(1/fps * 1000/1)

    print('Num. Frames = ', n_frames)
    print('Frame Rate = ', fps, ' frames per sec')

    # Need to creat window thread to destroy later
    cv2.startWindowThread()
    cv2.namedWindow('videoplay')

    for i in range(n_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame_img = cap.read()
        cv2.imshow('videoplay', frame_img)
        cv2.waitKey(frame_pause_ms)

    # When playing is done, delete the window
    cv2.destroyAllWindows()
    [cv2.waitKey() for i in range(4)]
    cap.release()

# play video, scroll forward/back
# sync with acc plot *or visa versa
   # interpolate with video, same sample rate
# buttons for annotation
   # - time
   # - annotation

if __name__ == '__main__':

    video_path = 'timer.mp4'

    play_video(video_path)
