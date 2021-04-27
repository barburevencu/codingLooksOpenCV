#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 9 17:18:17 2020

@author: Barbu

Added on Sat Nov 14
@looking time coding:  Basia
"""

import cv2, sys, csv, pandas as pd
from pathlib import Path

# Which video?
inputVideo = sys.argv[1]

# ID of subject to code
subjectID = int(input("Participant ID: "))

# experimental order of the subject
experimentalOrder = int(input("Experimental Order: "))

# Which task is to be coded?
task = int(input("Task (1 for preferential looking, 2 for looking times): "))

# Where to write?
outputFile = sys.argv[2].split('.')[0]

# =============================================================================
# # KEY SEMANTICS
# =============================================================================
# Advancing frames
UP = ord("i")
DOWN = ord("k")
LEFT = ord("j")
RIGHT = ord("l")
END = ord("e")

# Coding
LEFTGAZE = ord("a")
RIGHTGAZE = ord("d")
CENTERGAZE = ord("c")

BLINK = ord("b")

ONSCREEN = ord("o")

AWAY = ord("w")
UNKNOWN = ord("u")
NA = ord("n")

ENDOFPHASE = ord("E")
MISTAKE = ord("Z")

# Write to .csv
SAVE = ord("S")

# Quit
QUIT = ord("q")

# CSV file: check if it exists
myFile = Path(outputFile + ".csv")
if not myFile.exists():
    with open(outputFile + ".csv", 'w') as csvfile:
        lst = ["ID", "expOrder", "phase",
               "frameStart", "frameEnd", "gazeDirection"]
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(lst)

def keyToGaze(key):
    """
    Parameters
    ----------
    key: Key press in Unicode. One of ("l", "r", "c", "u", "d", "b", "n").

    Returns
    -------
    str
        Key press converted to Gaze Direction.

    """
    if key == LEFTGAZE:
        return "right"
    if key == RIGHTGAZE:
        return "left"
    if key == CENTERGAZE:
        return "center"
    if key == BLINK:
        return "blink"
    if key == ONSCREEN:
        return "looking"
    if key == AWAY:
        return "away"
    if key == UNKNOWN:
        return "unknown"
    if key == NA:
        return "NA"
    pass


def switch(currentPhase):
    if task == 1:
        if currentPhase == "baseline":
            return "highlight"
        elif currentPhase == "highlight":
            return "test"
        else:
            return "baseline"
    else:
        if currentPhase == "alternate1":
            return "alternate2"
        elif currentPhase == "alternate1":
            return "alternate2"

def code(videoName, outputFile):

    # Lists for data
    phase, frameStart, frameEnd, gazeDirection = [], [], [], []

    # assume you start from trial 1
    trial = 1

    # load video capture from file
    video = cv2.VideoCapture(videoName)

    # window name and position
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)

    total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(video.get(cv2.CAP_PROP_FPS), 3)
    print("totalNumberOfFrames: ", total)
    print("framesPerSecond: ", fps)

    if task == 1:
        currentPhase = "baseline"
    else:
        currentPhase = "alternate1"

    while video.isOpened():

        # Read video capture
        ret, frame = video.read()

        height, width, _ = frame.shape

        # Add current frame number to it
        currentFrame = int(video.get(cv2.CAP_PROP_POS_FRAMES))

        textPosition = (int(width/1.2), int(height/1.2))

        cv2.putText(frame, str(int(currentFrame)),
                    textPosition,
                    fontFace = cv2.FONT_HERSHEY_COMPLEX,
                    fontScale = 1.5,
                    color = (0, 165, 255),
                    thickness = 3)

        # Display each frame
        cv2.imshow("video", frame)

        # Show one frame at a time
        key = cv2.waitKey(0)

        # =============================================================================
        # CONTROL VIDEO
        # =============================================================================
        # ADVANCE 1 FRAME IF RIGHT-ARROW
        while key not in [QUIT, END,
                          UP, DOWN, LEFT, RIGHT,
                          LEFTGAZE, RIGHTGAZE, CENTERGAZE,
                          BLINK, ONSCREEN, AWAY, NA, UNKNOWN, ENDOFPHASE,
                          MISTAKE, SAVE]:
            key = cv2.waitKey(0)

        # STOP FRAME IF AT END-OF-FILE
        if key == RIGHT and currentFrame == total:
            video.set(1, currentFrame - 1)

        # GO BACK 1 FRAME IF LEFT-ARROW
        if key == LEFT:
            video.set(1, currentFrame - 2)

        # SKIP 100 FRAMES IF UP-ARROW
        elif key == UP:
            if (currentFrame + 59) < (total - 600):
                video.set(1, currentFrame + 59)
            else:
                video.set(1, currentFrame - 1)

        # GO BACK 50 FRAMES IF DOWN-ARROW
        elif key == DOWN:
            video.set(1, currentFrame - 31)

        # GO TO END-OF-VIDEO IF 'E'
        elif key == END:
            video.set(1, total - 1)

        # ====================================================================
        # CODE VIDEO
        # ====================================================================

            # do not advance frame
            video.set(1, currentFrame - 1)

        elif key == ENDOFPHASE:
            print("Frame " + str(currentFrame) + ": End of " + currentPhase)
            print("-----------------------")
            currentPhase = switch(currentPhase)
            print("Next command will start " + currentPhase + ".")
            frameEnd.append(currentFrame)
            video.set(1, currentFrame - 1)

        elif key in [LEFTGAZE, RIGHTGAZE, CENTERGAZE,
                     BLINK, ONSCREEN, AWAY, NA, UNKNOWN]:

            if frameStart and len(frameStart) != len(frameEnd):
                frameEnd.append(currentFrame - 1)
            
            frameStart.append(currentFrame)
            gazeDirection.append(keyToGaze(key))
            
            if key == LEFTGAZE:
                print("Frame " + str(currentFrame) + ": Baby's looking LEFT.")
            elif key == RIGHTGAZE:
                print("Frame " + str(currentFrame) + ": Baby's looking RIGHT.")
            elif key == CENTERGAZE:
                print("Frame " + str(currentFrame) + ": Baby's looking to the CENTER.")
            elif key == BLINK:
                print("Frame " + str(currentFrame) + ": Baby's BLINKING.")
            elif key == AWAY:
                print("Frame " + str(currentFrame) + ": Baby's looking AWAY.")
            elif key == NA:
                print("Frame " + str(currentFrame) + ": Start of HIGHLIGHT phase.")
            elif key == UNKNOWN:
                print("Frame " + str(currentFrame) + ": UNKNOWN gaze direction.")

            
            # do not advance frame
            video.set(1, currentFrame - 1)
            phase.append(currentPhase)

        elif key == MISTAKE:
            print("Undo last command.")
            if frameEnd:
                frameEnd.pop(-1)
            frameStart.pop(-1)
            gazeDirection.pop(-1)
            phase.pop(-1)
            video.set(1, currentFrame - 1)

        elif key == SAVE or key == QUIT:
            if key == SAVE:
                print("Saved progress to .csv")
            # create ID and expOrder column
            ID = [subjectID for i in range(len(phase))]
            expOrder = [experimentalOrder for i in range(len(phase))]


            if len(frameStart) == len(frameEnd) + 1:
                frameEnd.append(currentFrame)

            rows = zip(ID, expOrder, phase,
                       frameStart, frameEnd, gazeDirection)

            with open(outputFile + ".csv", 'a') as csvfile:
                wr = csv.writer(csvfile, dialect = 'excel')
                for row in rows:
                    wr.writerow(row)

            video.set(1, currentFrame - 1)

            if key == SAVE:
                phase, frameStart, frameEnd, gazeDirection = [], [], [], []

            else:
                break

    df = pd.read_csv(outputFile + ".csv", sep=',')

    # correct the trialNumber column if it got messed up
    phase = df["phase"].tolist()

    trial = 1
    trialNumber = []
    
    # Add Trial Number Column based on Phase information
    if task == 1:
        for i, j in zip(range(0, len(phase) - 1), range(1, len(phase))):
            trialNumber.append(trial)
            if phase[i] == "test" and phase[j] == "baseline":
                trial += 1
    else:
        for i, j in zip(range(0, len(phase) - 1), range(1, len(phase))):
            trialNumber.append(trial)
            if phase[i] !=  phase[j]:
                trial += 1

    trialNumber.append(trial)
    
    df['trialNumber'] = trialNumber

    # Rearrange column order for Preferential Looking
    if task == 1:
        cols = df.columns.tolist()
        
        # (ID, expOrder) + trialNumber + (phase, frameStart, frameEnd, gazeDirection)
        cols = cols[:2] + cols[-1:] + cols[2:-1]
        df = df[cols]

    # Turn frames into seconds & rearrange column order for Looking Time
    if task == 2:
        df['timeStart'] = df['frameStart'] / fps
        df['timeEnd'] = df['frameEnd'] / fps
        cols = df.columns.tolist()
        print(cols)
        
        # (ID, expOrder) + trialNumber + (frameStart, frameEnd) + (timeStart, timeEnd) + gazeDirection
        cols = cols[:2] + cols[-3:-2] + cols[3:5] + cols[-2:] + cols[5:6]

        df = df[cols]
        
    # Write to excel
    df.to_excel(outputFile + ".xlsx", index = False)
    
    # Release capture object
    video.release()

    # Exit and remove windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    code(inputVideo, outputFile)
