# Project Diary

## Contents
- [Project Diary](#project-diary)
  - [Contents](#contents)
  - [Weeks](#weeks)
    - [Week 1 (18/09/23)](#week-1-180923)
    - [Week 2 (25/09/23)](#week-2-250923)
    - [Week 3 (02/10/23)](#week-3-021023)
    - [Week 4 (09/10/23)](#week-4-091023)
    - [Week 5 (16/10/23)](#week-5-161023)
    - [Week 6 (23/10/23)](#week-6-231023)
    - [Week 7 (30/10/23)](#week-7-301023)
    - [Week 8 (6/10/23)](#week-8-61023)
    - [Week 9 (13/11/23)](#week-9-131123)
    - [Week 10 (20/11/23)](#week-10-201123)


## Weeks

### Week 1 (18/09/23)

 - (Tue 19) Attended first lecture 
 - (Thu 21) Started reading Reinforcement Learning in 'Machine Learning' by Tom Mitchell
 - (Fri 22) Finished reading Reinforcement Learning in 'Machine Learning' by Tom Mitchell

### Week 2 (25/09/23)

 - (Mon 25) Decided on project idea 
   - Started draft project plan 
   -  Abstract
   -  Risks
-  (Tue 26) First meeting with Anand
   - Started putting together timeline
   - Started reading Reinforcement Learning An Introduction by Richard S. Sutton and Andrew G. Barto
 - (Wed 27) 
   - Attended second lecture
   - moved project plan over to LaTeX
 - (Thu 28) Worked on project plan report 
   - improved bibliography

### Week 3 (02/10/23)

 - (Tue 3) worked on project plan
   - Put together risks section 
   - put together timeline 
 - (Wed 4) submitted project plan to Anand
 - (Thu 5) Finished project plan
   - Improved abstract
   - improved bibliography

### Week 4 (09/10/23)

 - (Wed 11) Gitlab
   - Attended lecture about gitlab
   - Moved Code to GitLab 
     - setup credentials
     - updated remotes
     - pushed code
 - (Thu 12) Created Initial Interim report from template
   - Finished chapter one from Sutton Barto book

### Week 5 (16/10/23)

 - (Mon 16) Continued reading Sutton Barto book
   - chapter 2 and some of chapter 3
 - (Wed 18) Continued reading
   - finished Chapter 3
   - attended lecture about testing
 - (Thu 19)
   - Second Meeting with Anand
 - (Fri 20) Continued reading read subsections on policy improvement

### Week 6 (23/10/23)

 - (Mon 23) 
   - Continued reading Sutton Barto book
     - read chapters 4,6 and skimmed 5
   - Met Anand to discuss my project plan

### Week 7 (30/10/23)

 - (Thu 2) 
   - Started MDP Report
   - Third Meeting with Anand
 - (Weekend 4-5)
   - Completed MDP Report

### Week 8 (6/10/23)

 - (Mon 6) Started report on the policy and value functions
 - (Tue 7) Completed policy and value report
 - (Wed 8) 
   - Completed policy and value report
   - Started Q-learning report
 - (Thu 9) 
   - Completed Q-learning report
   - Started code setup
 - (Weekend 10-11) continued setting up code

### Week 9 (13/11/23)

 - (Mon 13) 
   - Completed code setup 
 - (Tue 14) 
   - Started vertical slice
 - (Wed 15)
   - Started writing collection dynamics method
 - (Thu 16)
   - Completed collection dynamics
   - Started implementing value iteration
   - Fourth meeting with Anand
 - (Fri 17)
   - completed value iteration agent

### Week 10 (20/11/23)

 - (Mon 20) 
   - Created controllers to tie view and model together.
   - Tried to display grid with canvas approach
     - ran into rendering limitations, with many rectangles rectangles kivy started to have issues with rendering the icons.
 - (Tue 21) tried widget based approach
   - Tried using kivy's layout widgets to display the grid
   - while the icons were no longer an issue positioning the grid became impossible 
   - investigated kivy alternatives
 - (Wed 22) Pivoted to using tkinter 
   - remade exiting UI in tkinter and updated tooling for working with tkinter
   - completed grid world display widget
 - (Thu 23)
   - Added button that progresses the state over time.
   - Created methods to provide the value information to the view, allowing for visualisation.
   - 