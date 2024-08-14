from playsound import playsound as make_sound
import threading
import cv2 as cv
import imutils
import os


def alert():
    global alarm

    for _ in range(int(warning_count)):
        if not alarm_mode:
            break

        print(f"\033[1;31m{'*' * 10} WARNING {'*' * 10}\033[0m")
        make_sound(sound_path)

    alarm = False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clear_screen()

print("\033[1;32m")
print("╔════════════════════════════════╗")
print("║ How many warnings do you want? ║")
print("╚════════════════════════════════╝")
warning_count = int(input("\033[1;33m→ \033[0m"))

alarm = False
alarm_mode = False
alarm_counter = 0
cam_width, cam_height = (1280, 720)  # camera resolution
sound_path = "Computer Vision/motion-detection-advance/sound.mp3"
gaussian_frame_size = (31, 31)
gaussian_frame_size2 = (7, 7)
deviation = 0
thresh_value, max_pixel_value = (30, 255)
movement_value = 500

# camera access
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)

# Verify that the camera is open
if not cam.isOpened():
    print("\033[1;31mError: Could not access the camera.\033[0m")
    exit()

# Capture the first frame
ret, start_frame = cam.read()
if not ret or start_frame is None:
    print(
        "\033[1;31mError: Could not read the initial frame from the camera.\033[0m")
    exit()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv.cvtColor(start_frame, cv.COLOR_BGR2GRAY)
start_frame = cv.GaussianBlur(start_frame, gaussian_frame_size, deviation)

print("\n\033[1;36m═════════════════════════════════════════")
print("Press \033[1;32ms\033[1;36m to START and \033[1;31mq\033[1;36m to STOP")
print("═════════════════════════════════════════\033[0m")

while True:
    ret, frame = cam.read()
    if not ret or frame is None:
        print("\033[1;31mError: Could not read a frame from the camera.\033[0m")
        break

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_blw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_blw = cv.GaussianBlur(frame_blw, gaussian_frame_size2, deviation)

        frame_difference = cv.absdiff(frame_blw, start_frame)
        threshold = cv.threshold(
            frame_difference, thresh_value, max_pixel_value, cv.THRESH_BINARY)[1]
        start_frame = frame_blw

        if threshold.sum() > movement_value:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv.imshow("Camera", threshold)
    else:
        cv.imshow("Camera", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=alert).start()

    key_press = cv.waitKey(30)
    if key_press == ord("s"):
        alarm_mode = not alarm_mode
        alarm_counter = 0

    if key_press == ord("q"):
        alarm_mode = False
        break

cam.release()
cv.destroyAllWindows()

print("\n\033[1;31m═══════════════════════════")
print("Program Terminated!")
print("═══════════════════════════\033[0m")
