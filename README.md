# Project Name
codingLooksOpenCV

# Requirements
- Python 3.8 or above
- OpenCV-python-headless 4.4 or above

We recommend installing the Anaconda distribution via Homebrew following [these instructions](https://medium.com/ayuth/install-anaconda-on-macos-with-homebrew-c94437d63a37), then installing ```opencv``` via ```pip install opencv-python-headless```.

# Description
A program for coding preferential looking studies for infancy research from video files (think manual offline eyetracker). 

For now, you can choose to video code one of the two experimental structures.

## 1 Preferential looking
If you choose preferential looking, the program assumes that each trial has the following structure:

Trial *n*: Baseline

Trial *n*: Highlight

Trial *n*: Test

## 2 Looking time
If you choose looking time, the program assumes that each trial has the following structure:

Trial *n*: Test

# Usage
## Starting the program
The program can be launched from the terminal/command line. After changing the working directory to the location of ```openCV.py``` and of the video to be coded, run:
```
python openCV.py NAME-OF-VIDEO.mp4 NAME-OF-OUTPUT-FILE.xlsx
```

**Important: The video needs to be in ```.mp4``` format.**

### Initializing relevant parameters
First, the program will ask you to pass it the *subject ID* and the *experimental order*. This information will be appended to the output file, and will be handy in data analysis to match the observation to information about experimental manipulation.

Them, it will ask you to specify which *task* you want to code (1: preferential looking, 2: looking time).

### Video view
The first frame of the video will then appear on your screen, with the frame number superimposed in orange. 

#### Video Navigation
Use the keyboard arrows to navigate:

<kbd>&#8594;</kbd>: Advance one frame   
<kbd>&#8592;</kbd>: Go back one frame    
<kbd>&#8593;</kbd>: Skip 100 frames  
<kbd>&#8595;</kbd>: Go back 50 frames 

## Coding looking behavior

### Coding: Key Semantics
#### Gaze
<kbd>l</kbd> OR <kbd>a</kbd>: **l**eft gaze  
<kbd>r</kbd> OR <kbd>d</kbd>: **r**ight gaze  
<kbd>c</kbd> OR <kbd>s</kbd>: **c**enter gaze  
<kbd>b</kbd>: **b**link  
<kbd>o</kbd>: look-**o**nscreen  
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

### Instructions how to code looking behavior
The program needs to know the following things:
1. When participant's gaze shifts.
2. When a phase ends.

Every time you press one of the GAZE keys, the program will store several variables, which represent: (i) track of current phase (e.g., baseline, highlight, or test); (ii) at which frame the key was pressed at; (iii) the specific gaze coded (left, right, center, etc.). In addition, the program also computes the end frame of the previous window, by subtracting 1 from the current frame.

### Preferential looking
*Example.* Suppose the timings are as follows for the subject you're coding:
1. Baseline (Trial 1): Frames 251-300
2. Highlight (Trial 1): Frames 351-450
3. Test (Trial 1): Frames 551-625
4. Baseline (Trial 2): Frames 976-1000
5. Highlight (Trial 2): Frames 1033-1100
6. Test (Trial 2): Frames 1170-1205

**To code one subject, you need to:**

1. Go to the first frame of the first phase (Trial 1 Baseline; Frame 251), and code where the participant is looking in that frame (left, right, center, blink, look-away, or unknown) by pressing the corresponding key.
2. Advance video until you reach a frame where the participant shifts gaze.  
(If subject was looking **left** at Frame 251, and shifts to **center** at Frame 275, you need to press <kbd>l</kbd>/<kbd>a</kbd> at Frame 251 in Step 1, and <kbd>c</kbd>/<kbd>s</kbd> at Frame 275 in Step 2.)
3. When you reach the end of the phase (Frame 300), press <kbd>SHIFT</kbd> + <kbd>e</kbd> to mark the **E**nd of the current phase. Internally, the program handles the baseline-highlight-test automatically.
4. Press <kbd>SHIFT</kbd> + <kbd>f</kbd>. The program will write what you have inputted so far to a ```.csv``` file. 
5. Advance to the next phase (Trial 1 highlight) and repeat.

That's it.

After you save your coding (step 4), you can  quit the program before finishing one whole subject, and continue coding later on.

**What to do when you make a mistake?**

If you press a wrong non-inert key or change your mind, you can signal you have made a mistake by pressing <kbd>SHIFT</kbd> + <kbd>m</kbd>, without needing to go back to the frame where you made the mistake. The program will simply remove the last command you gave it. Pressing an inert key by mistake should **not** be corrected.

**What happens when you quit the program?**

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

### Looking time
*Example.* Suppose the timings are as follows for the subject you're coding:
1. Familiarization 1 (Trial 1): Frames 251-300
2. Familiarization 2 (Trial 2): Frames 351-450
3. Test 1 (Trial 3): Frames 551-625
4. Test 2 (Trial 4): Frames 976-1000

**To code one subject, you need to:**
1. Go to the first frame of the first phase (Familiarization 1: Frame 251), and code where the participant is looking in that frame  by pressing the corresponding key (look onscreen <kbd>o</kbd>, look-away <kbd>w</kbd>, or unknown <kbd>u</kbd>).
2. Advance video until you reach a frame where the participant shifts gaze.  
(e.g., If subject was looking **onscreen** at Frame 251, and shifts to **away** at Frame 275, you need to press <kbd>o</kbd> at Frame 251 in Step 1, and <kbd>w</kbd> in Step 2.)
3. When you reach the end of the phase (Frame 300), press <kbd>SHIFT</kbd> + <kbd>e</kbd> to mark the **E**nd of the current phase. Internally, the program will switch to the next trial.
4. Press <kbd>SHIFT</kbd> + <kbd>f</kbd>. The program will write what you have inputted so far to a ```.csv``` file. 
5. Advance to the next phase (Trial 1 highlight) and repeat.

That's it.

After you save your coding (step 4), you can  quit the program before finishing one whole subject, and continue coding later on.

**What to do when you make a mistake?**

If you press a wrong non-inert key or change your mind, you can signal you have made a mistake by pressing <kbd>SHIFT</kbd> + <kbd>m</kbd>, without needing to go back to the frame where you made the mistake. The program will simply remove the last command you gave it. Pressing an inert key by mistake should **not** be corrected.

**What happens when you quit the program?**

When you quit the program, an excel file will be written to the current working directory (the one where ```openCV.py``` and video are located), which will have the following structure:

| ID| expOrder | trialNumber | frameStart | frameEnd | timeStart | timEnd | gazeDirection |
|:-:|:--------:|:-----------:|:----------:|:--------:|:---------:|:------:|:-------------:|   
| 1 | 7        | 1           | 251        | 274      | 4.204     | 4.589  | onscreen      |
| 1 | 7        | 1           | 275        | 300      | 4.606     | 5.025  | away          |
| 1 | 7        | 2           | 351        | 450      | 5.879     | 7.537  | onscreen      |

Based on the number of frames/second of the video (in this example, 59.7), the output includes two columns, ```timeStart``` and ```timeEnd```, which turn the corresponding frame columns into seconds.
