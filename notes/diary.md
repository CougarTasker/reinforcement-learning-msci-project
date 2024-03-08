<!-- omit in toc -->
# Project Diary

<!-- omit in toc -->
## Contents
- [Week 01 (18/09/23)](#week-01-180923)
- [Week 02 (25/09/23)](#week-02-250923)
- [Week 03 (02/10/23)](#week-03-021023)
- [Week 04 (09/10/23)](#week-04-091023)
- [Week 05 (16/10/23)](#week-05-161023)
- [Week 06 (23/10/23)](#week-06-231023)
- [Week 07 (30/10/23)](#week-07-301023)
- [Week 08 (06/10/23)](#week-08-061023)
- [Week 09 (13/11/23)](#week-09-131123)
- [Week 10 (20/11/23)](#week-10-201123)
- [Week 11 (27/11/23)](#week-11-271123)
- [Week 12 (04/12/23)](#week-12-041223)
- [Christmas Break](#christmas-break)
- [Week 17 (08/01/24) first week of term](#week-17-080124-first-week-of-term)
- [Week 18 (15/01/24)](#week-18-150124)
- [Week 19 (22/01/24)](#week-19-220124)
- [Week 20 (29/01/24)](#week-20-290124)
- [Week 21 (05/02/24)](#week-21-050224)
- [Week 22 (12/02/24)](#week-22-120224)
- [Week 23 (19/02/24)](#week-23-190224)
- [Week 25 (04/03/24)](#week-25-040324)

<!-- omit in toc -->
## Weeks

### Week 01 (18/09/23)

 - (Tue 19) Attended first lecture 
 - (Thu 21) Started reading Reinforcement Learning in 'Machine Learning' by Tom Mitchell
 - (Fri 22) Finished reading Reinforcement Learning in 'Machine Learning' by Tom Mitchell

### Week 02 (25/09/23)

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

### Week 03 (02/10/23)

 - (Tue 03) worked on project plan
   - Put together risks section 
   - put together timeline 
 - (Wed 04) submitted project plan to Anand
 - (Thu 05) Finished project plan
   - Improved abstract
   - improved bibliography

### Week 04 (09/10/23)

 - (Wed 11) Gitlab
   - Attended lecture about gitlab
   - Moved Code to GitLab 
     - setup credentials
     - updated remotes
     - pushed code
 - (Thu 12) Created Initial Interim report from template
   - Finished chapter one from Sutton Barto book

### Week 05 (16/10/23)

 - (Mon 16) Continued reading Sutton Barto book
   - chapter 2 and some of chapter 3
 - (Wed 18) Continued reading
   - finished Chapter 3
   - attended lecture about testing
 - (Thu 19)
   - Second Meeting with Anand
 - (Fri 20) Continued reading read subsections on policy improvement

### Week 06 (23/10/23)

 - (Mon 23) 
   - Continued reading Sutton Barto book
     - read chapters 4,6 and skimmed 5
   - Met Anand to discuss my project plan

### Week 07 (30/10/23)

 - (Thu 02) 
   - Started MDP Report
   - Third Meeting with Anand
 - (Weekend 4-5)
   - Completed MDP Report

### Week 08 (06/10/23)

 - (Mon 06) Started report on the policy and value functions
 - (Tue 07) Completed policy and value report
 - (Wed 08) 
   - Completed policy and value report
   - Started Q-learning report
 - (Thu 09) 
   - Completed Q-learning report
   - Started code setup
 - (Weekend 10-11) continued setting up code

### Week 09 (13/11/23)

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
   - Created methods to provide the Q-value information to the view, allowing for visualisation.
 - (Fri 24)
   - Started adding Q-value visualisation code, 
   - Optimised value iteration code with numba
   - Reworked how cells are provided their information

### Week 11 (27/11/23)

 - (Mon 27) Created tooltip to provide state value information and fixed origin inconsistency from the move to tkinter.
 - (Tue 28) Completed system for allowing the user to select between different types of displays
 - (Wed 29)
   - Improved code `README` and improved usability 
   - Implemented the Q-learning agent with 
   - Added simultaneous agents to speed up learning
   - Added opening to project report
 - (Thu 30)
   - Improved Interim Report
   - Fifth meeting with Anand
     - Anand noticed how the simultaneous agents deviated for the literature
 - (Fri 01) Refactor
   - Removed the simultaneous agents feature
   - focused on Improving performance in other ways:
     - Split MVC across different processes to avoid the GIL
     - Improved rendering approach with Pillow no more odd layout and widgets
   - Started making presentation
 - (Sat 02)
   - Completed presentation slides
   - Practised presentation

### Week 12 (04/12/23)
 - (Mon 04)
   - Practised presentation
   - Gave presentation
 - (Fri 08)
   - Prepared work for Interim submission 


### Christmas Break 

 - (Mon 11) Documentation Improvements
   - Setup static documentation site generation
   - Improved readme
 - (Fri 15) Quality of life improvements
   - Improved application lifecycle
   - Investigated graphics performance bottleneck
   - Tested different GUI framework

### Week 17 (08/01/24) first week of term

 - (Wed 10) Completed migration to new GUI framework

### Week 18 (15/01/24)

 - (Mon 15) Updated IPC method to reduce overhead and latency 
 - (Fri 19) Improved Software Engineering section of the report

### Week 19 (22/01/24)

 - (Wed 24) 
   - Started Implementing different exploration strategies for Q-learning
     - separating the exploration strategy from the Q-learning agent 
   - Added more detail to report
 - (Thu 25) 
 - (Fri 26)
   - Reworked parts of the program to make different strategies configurable
   - First Term two meeting with Anand. where we discussed what the term two focus of the project should be
  
### Week 20 (29/01/24)

 - (Mon 29) worked on dynamics to improve consistency for comparisons
 - (Tue 30) Implemented Upper confidence bound exploration strategy
 - (Wed 31) added statistics system for recording and displaying the effectiveness of different algorithms.
 - (Thu 01) 
   - started hyper parameter tuning system 
   - reviewed readings from Anand. 
 - (Fri 02) Attended extension focus meeting.

### Week 21 (05/02/24)

This week was spent on a major overhaul to the configuration system to support hyper-parameters for tuning.

 - (Mon 05) started investigating what changes were necessary
 - (Wed 07) started to rework the configuration system
   - adding missing parameters 
   - reorganised configuration objects 
   - created hyper-parameter listings
 - (Fri 09) Updated top level entities
   - reworked top level entities to make it easier to inject different parameters
   - separated out top level entities to manage there complexity and to ease in their use separate from the main learning system
 - (Sat 10) Fixed teething issues, updated tests 

### Week 22 (12/02/24)

 - (Mon 12) Created UI for displaying the effect of hyper-parameters
   - added control to pick a parameter to start report generation
   - added progress feedback during the report generation
 - (Tue 13) 
   - Bug fixes
   - added epsilon discounting to the epsilon greedy strategy, so that it can compete more fairly with UCB
 - (Wed 14) Added hyper-parameter random search, to find the best parameters over time.
 - (Thu 15) Created display for the random search results
  
### Week 23 (19/02/24)

 - (Wed 21) 
   - added functionality for saving graphs to disk for use in the report or otherwise.
   - Researched the MF-BPI algorithm
 - (Thu 22) Adapted the MF-BPI algorithm to work with my application 
 - (Fri 23) Attended third term-two supervisor meeting 
   - continued to analyse MF-BPI algorithm and better integrate it with the application.

### Week 25 (04/03/24)

 - (Wed 06) Started working on final report
   - scaffolded the structure of the final report
   - started researching professional issues found case study 
 - (Thu 07) Worked on professional issues section
   - wrote introduction and found sources 
 - (Fri 08) Completed first draft of professional issues section