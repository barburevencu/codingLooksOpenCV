#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:18:17 2020

@author: Barbu
"""

import cv2, sys, csv, pandas as pd, os
from pathlib import Path

# Which video?
inputVideo = sys.argv[1]

# Does the user want it resized?
try:
    resizeParam = float(sys.argv[3])
except:
    resizeParam = 1

# Where to write?
outputFile = sys.argv[2]


# =============================================================================
# # KEY SEMANTICS
# =============================================================================
# Advancing frames
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
END = ord("e")

# Coding
LEFTGAZE = ord("l")
LEFTGAZE2 = ord("a")

RIGHTGAZE = ord("r")
RIGHTGAZE2 = ord("d")

CENTERGAZE = ord("c")
CENTERGAZE2 = ord("s")

UPGAZE = ord("w")
BLINK = ord("b")

AWAY = ord("y")
NA = ord("n")

ENDOFPHASE = ord("E")

MISTAKE = ord("M")
BASELINE = ord("B")
TEST = ord("T")
HIGHLIGHT = ord("H")

# Write to .csv
FLUSH = ord("F")

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
    if key == LEFTGAZE or key == LEFTGAZE2:
        return "right"
    if key == RIGHTGAZE or key == RIGHTGAZE2:
        return "left"
    if key == CENTERGAZE or key == CENTERGAZE2:
        return "center"
    if key == UPGAZE:
        return "up"
    if key == BLINK:
        return "blink"
    if key == AWAY:
        return "away"
    if key == NA:
        return "NA"
    pass


def switch(currentPhase):
    if currentPhase == "baseline":
        return "highlight"
    elif currentPhase == "highlight":
        return "test"
    else:
        return "baseline"

def code(videoName, outputFile):
    
    # Lists for data
    phase, frameStart, frameEnd, gazeDirection = [], [], [], []
    
    # assume you start from trial 1
    trial = 1
    
    # load video capture from file
    video = cv2.VideoCapture(videoName)
    
    # window name and position
    cv2.namedWindow("video")
    
    total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(video.get(cv2.CAP_PROP_FPS), 3)
    print("totalNumberOfFrames: ", total)
    print("framesPerSecond: ", fps)
    
    currentPhase = "baseline"
    
    while video.isOpened():
        
        # Read video capture
        ret, frame = video.read()
        
        height, width, _ = frame.shape

        newHeight = int(height // resizeParam)
        newWidth = int(width // resizeParam)
        
        frame = cv2.resize(frame, (newWidth, newHeight))
        
        # Add current frame number to it
        currentFrame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        
        cv2.putText(frame, str(int(currentFrame)), (800, 500), 
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
                          LEFTGAZE2, RIGHTGAZE2, CENTERGAZE2,
                          UPGAZE, BLINK, AWAY, NA, 
                          BASELINE, TEST, ENDOFPHASE,
                          MISTAKE, FLUSH]:
            key = cv2.waitKey(0)
        
        # STOP FRAME IF AT END-OF-FILE
        if key == RIGHT and currentFrame == total:
            video.set(1, currentFrame - 1)
        
        # GO BACK 1 FRAME IF LEFT-ARROW
        if key == LEFT:
            video.set(1, currentFrame - 2)
        
        # SKIP 100 FRAMES IF UP-ARROW
        elif key == UP:
            video.set(1, currentFrame + 99)
        
        # GO BACK 50 FRAMES IF DOWN-ARROW
        elif key == DOWN:
            video.set(1, currentFrame - 51)
        
        # GO TO END-OF-VIDEO IF 'E'
        elif key == END:
            video.set(1, total - 1)
        
        # ====================================================================
        # CODE       
        # ====================================================================
        elif key in [BASELINE, HIGHLIGHT, TEST]:
            if key == BASELINE:
                currentPhase = "baseline" 
            elif key == HIGHLIGHT:
                currentPhase = "highlight"
            else:
                currentPhase = "test"
            # do not advance frame
            video.set(1, currentFrame - 1)            
        
        elif key == ENDOFPHASE:
            currentPhase = switch(currentPhase)
            frameEnd.append(currentFrame)
            video.set(1, currentFrame - 1) 
            
        elif key in [LEFTGAZE, RIGHTGAZE, CENTERGAZE,
                     LEFTGAZE2, RIGHTGAZE2, CENTERGAZE2,
                     UPGAZE, BLINK, AWAY, NA]:

            if frameStart and len(frameStart) != len(frameEnd):
                frameEnd.append(currentFrame - 1)
            
            frameStart.append(currentFrame)
            gazeDirection.append(keyToGaze(key))
            
            # do not advance frame
            video.set(1, currentFrame - 1)
            phase.append(currentPhase)
            
        elif key == MISTAKE:
            if frameEnd:
                frameEnd.pop(-1)
            frameStart.pop(-1)
            gazeDirection.pop(-1)
            phase.pop(-1)
            video.set(1, currentFrame - 1) 
    
        elif key == FLUSH or key == QUIT:
                       
            # create ID and expOrder column
            ID = [int(sys.argv[4]) for i in range(len(phase))]
            expOrder = [int(sys.argv[5]) for i in range(len(phase))]
        
            
            if len(frameStart) == len(frameEnd) + 1:
                frameEnd.append(currentFrame)
            
            rows = zip(ID, expOrder, phase, 
                       frameStart, frameEnd, gazeDirection)      
            
            with open(outputFile + ".csv", 'a') as csvfile:
                wr = csv.writer(csvfile, dialect = 'excel')
                for row in rows:
                    wr.writerow(row)
            
            video.set(1, currentFrame - 1) 
            
            if key == FLUSH:
                phase, frameStart, frameEnd, gazeDirection = [], [], [], []
                
            else:
                break
    
    
    df = pd.read_csv(outputFile + ".csv", sep=',')
    
    # correct the trialNumber column if it got messed up
    phase = df["phase"].tolist()

    trial = 1
    trialNumber = []    

    for i, j in zip(range(0, len(phase) - 1), range(1, len(phase))): 
        trialNumber.append(trial)
        if phase[i] == "test" and phase[j] == "baseline":
            trial += 1
        
    trialNumber.append(trial)

    df['trialNumber'] = trialNumber
    
    # rearrange column order
    cols = df.columns.tolist()
    cols = cols[0:2] + cols[-1:] + cols[2:-1]
    df = df[cols]
    
    # write to excel
    df.to_excel(outputFile + ".xlsx", index = False)
        
    # os.remove(outputFile + ".csv")
    
    # Release capture object
    video.release()
    
    # Exit and destroy all windows
    cv2.destroyAllWindows()

code(inputVideo, outputFile)