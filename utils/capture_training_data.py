from __future__ import print_function
import sys
import cv2
import time
import os
from datetime import datetime
import pickle
import csv

width = 640 # Our capture width
height = 360 # Our capture height

show_preview = False # Default to false

# Should we show a preview of the video stream
if ("-s" in sys.argv) or ("--show-preview" in sys.argv):
    print("Will show preview when ready...")
    show_preview = True


# Holds all our individual video frame filenames/data
frames = []

# Make the jpg folder of current date/time
jpg_path = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
print("Making new jpg directory at: " + jpg_path)

if not os.path.exists(jpg_path):
    os.makedirs(jpg_path)

def main(argv):
    frame_number = 0; # Start at 0 frames
    
    # Capture from first available camera (0)
    cap = cv2.VideoCapture(0)
    
    # Set the capture width/height
    cap.set(3, width)
    cap.set(4, height)
    
    # Pull frames as fast as we can
    while True:
        # Pull a frame
        ret, img = cap.read()

        # If preview is enabled, show the frame
        # Super useful to use with x11 forwarding via ssh
        if (show_preview):
            cv2.imshow("input", img)
        
        # Placeholder for each list item/frame
        frame = {"jpg": "", "steering": 0.0, "throttle": 0.0}

        # Set the current filename to frame number & write it
        frame["jpg"] = str(frame_number) + ".jpg"
        cv2.imwrite(jpg_path + "/" + frame["jpg"], img)
        
        # TODO (placeholder) - will implement soon, static values for testing
        steering = 1.3
        throttle = -1.2
        
        # Save the control values and add current frame & data to list
        frame["steering"] = steering
        frame["throttle"] = throttle
        frames.append(frame)
        #print("Saved Frame: " + str(frame))
        
        # Let us know we saved a frame
        print("Captured and saved {} frames...".format(frame_number), end='\r')
        
        # Increase frame number by 1
        frame_number += 1
        
        # Check if we should exit (press 'q') 
        key = cv2.waitKey(10)
        if key == 1048689:
            quit_program()
            print("Exiting ('q' key pressed)")
            break

    # Properly close everything on exit
    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()

def quit_program():
    if ("-c" in sys.argv) or ("--output-csv" in sys.argv):
        with open(jpg_path + "/frame_data.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["jpg", "steering", "throttle"])
            for frame in frames:
                csvwriter.writerow([frame["jpg"], frame["steering"], frame["throttle"]])
            print("Saved a csv in {}/frame_data.csv".format(jpg_path))

    if ("-p" in sys.argv) or ("--output-pickle" in sys.argv):
        pickle.dump(frames, open(jpg_path + "/frame_data.pickle", "wb"))
        print("Saved a pickle in {}/frame_data.pickle".format(jpg_path))

    print("\nSaved {} (jpg) frames and stored them in {}".format(len(frames), jpg_path))

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        quit_program()
        print("Exiting (keyboard interrupt)")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
