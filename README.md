# Project Name
codingLooksOpenCV

# Description
A program for coding preferential looking studies for infancy research from video files (think manual offline eyetracker).
For now, the program assumes the following experimental structure:
1. Trial 1: Baseline
2. Trial 1: Highlight
3. Trial 1: Test
1. Trial 2: Baseline
2. Trial 2: Highlight
3. Trial 2: Test
4. ...

# Usage
## Starting the program
The program can be launched from the terminal/command line. After changing the working directory to the location of ```openCV.py``` and of the video to be coded, run:
```
python openCV.py NAME-OF-VIDEO.mp4 NAME-OF-OUTPUT-FILE.xlsx
```

## Initializing relevant parameters
First, the program will ask you to pass it the subject ID, then the experimental order. This information will be appended to the output file, and will come handy in data analysis to match the observation to information about experimental manipulation.

## Video
The first frame of the video will then appear on your screen, with the frame number superimposed in orange. 

### Video Navigation
Use the keyboard arrows to navigate:

<kbd>&#8594;</kbd>: Advance one frame   
<kbd>&#8592;</kbd>: Go back one frame    
<kbd>&#8593;</kbd>: Skip 100 frames  
<kbd>&#8595;</kbd>: Go back 50 frames  

### Coding: Key Semantics
#### Gaze
<kbd>l</kbd> OR <kbd>a</kbd>: **l**eft gaze  
<kbd>r</kbd> OR <kbd>d</kbd>: **r**ight gaze  
<kbd>c</kbd> OR <kbd>s</kbd>: **c**enter gaze  
<kbd>b</kbd>: **b**link  
<kbd>w</kbd>: look-a**w**ay  
<kbd>u</kbd>: **u**nknown  
<kbd>n</kbd>: **NA**  

#### Other
<kbd>SHIFT</kbd> + <kbd>e</kbd>: **E**nd of current trial phase  
<kbd>SHIFT</kbd> + <kbd>m</kbd>: **M**istake  

#### Data & Global Esc
<kbd>SHIFT</kbd> + <kbd>f</kbd>: **F**lush to .csv  
<kbd>q</kbd>: **q**uit program (and get excel file)

All other keys are inert.

## Logic
The program needs to know the following things:
1. When participant's gaze shifts.
2. When a phase ends.

Every time you press one of the GAZE keys, the program will store several variables, which represent: (i) track of current phase (baseline, highlight, or test); (ii) at which frame the key was pressed at; (iii) the specific gaze coded (left, right, center, etc.). In addition, the program also computes the end frame of the previous window, by subtracting 1 from the current frame.

### Example
Suppose the timings are as follows for the subject you're coding:
1. Baseline (Trial 1): Frames 251-300
2. Highlight (Trial 1): Frames 351-450
3. Test (Trial 1): Frames 551-625
4. Baseline (Trial 2): Frames 976-1000
5. Highlight (Trial 2): Frames 1033-1100
6. Test (Trial 2): Frames 1170-1205

To code one subject, you need to:
1. Go to the first frame of the first phase (Trial 1 Baseline; Frame 251), and code where the participant is looking in that frame (left, right, center, blink, look-away, or unknown) by pressing the corresponding key.
2. Advance video until you reach a frame where the participant shifts gaze.  
(If subject was looking **left** at Frame 251, and shifts to **center** at Frame 275, you need to press <kbd>l</kbd>/<kbd>a</kbd> at Frame 251 in Step 1, and <kbd>c</kbd>/<kbd>s</kbd> at Frame 275 in Step 2.)
3. When you reach the end of the phase (Frame 300), press <<kbd>SHIFT</kbd> + <kbd>e</kbd> to mark the **E**nd of the current phase. Internally, the program handles the baseline-highlight-test automatically.
4. Advance to the next phase (Trial 1 highlight) and repeat.

That's it.

If you press a wrong non-inert key or change your mind, you can signal you have made a mistake by pressing <kbd>SHIFT</kbd> + <kbd>m</kbd>, without needing to go back to the frame where you made the mistake. The program will simply remove the last command you gave it. Pressing an inert key by mistake should **not** be corrected.

Every time you press <kbd>SHIFT</kbd> + <kbd>f</kbd>, the program will write what you have inputted so far to a ```.csv``` file. This allows you to quit the program before finishing one whole subject, and continuing later on.

When you quit the program, an excel file will be written to the current working directory (the one where ```openCV.py``` and video are located), which will have the following structure:
| ID| expOrder | trialNumber |    phase  | frameStart | frameEnd | gazeDirection |
|:-:|:--------:|:-----------:|:---------:|:----------:|:--------:|:-------------:|   
| 1 | 7        | 1           | baseline  | 251        | 274      | left          |
| 1 | 7        | 1           | baseline  | 275        | 300      | center        |
| 1 | 7        | 1           | highlight | 351        | 450      | ```NA```      |
| 1 | 7        | 1           | test      | 551        | 589      | right         |
| 1 | 7        | 1           | test      | 590        | 625      | away          |
| 1 | 7        | 2           | baseline  | 976        | 981      | left          |
| 1 | 7        | 2           | baseline  | 982        | 1000     | unknown       |
| 1 | 7        | 2           | highlight | 1033       | 1100     | ```NA```      |
| 1 | 7        | ...         | ...       | ...        | ...      | ...           |
