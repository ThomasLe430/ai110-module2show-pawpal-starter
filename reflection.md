# PawPal+ Project Reflection

## 1. System Design

A user should be able to add their pets into the system, add tasks into the Scheduler, and describe their availability and priorities.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

 Given the core functionality, the main objects needed for the system are: User, Pet, Task, and Scheduler. The User class needs to store information about pets and time restrictions/preferences they may have and add pets + tasks into the Scheduler. The Pet class will be linked to an owner, tasks associated with it, and necessary attributes of the pet. The Task class will store information about each task and support adding, editing, and deleting functionality. Finally, the scheduler holds information about tasks, pets, and users and can create a schedule for the user. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After asking the AI (Claude Code) for a design review, I changed some of the attributes of the system. In my first iteration, I had three classes (users, pets, and planner) able to add tasks. I thought this was disorganized, so I followed the AI's suggestion of only having pet own the add and remove task functionality. Additionally, I followed its recoommendation to add dataclasses for availability windows and scheduled entries, which I agree with in order to make the implementation easier. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduled considers the due date and priority of each task. Tasks that are due sooner and scheduled first, then are managed by priority. I decided to do it this way because it made sense to knock out one-time, urgent tasks then deal with the recurring tasks second. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is choosing to display a weekly schedule over a daily or monthly schedule. I chose this because I wanted to avoid making the app just another calendar app where you add tasks to calendar dates. Instead, I wanted it to create a weekly schedule that the user can actually use to balance and sort priorities, rather than visualize tasks (similar to Google Calendar). 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude code to design the architecture of the program, talk through algorithms (primarily creating schedule), front end display and form collection, debugging, and creating tests. The interactions that were the most helpful for me were the algorithm discussions because it was useful to get feedback on my thinking and what improvements I could make. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion was when it asked to make it so tasks can be added by calendar date rather than weekly basis. I rejected this because I wanted the app to focus on a weekly schedule so that it could be more helpful for the user. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the behavior of adding tasks and sorting/filtering them. I decided these were important because adding tasks is the core functionality of the website, and likely the most error prone. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

My scheduler can likely handle basic inputs, but there are certainly edge cases I did not consider. For example, I did not have time to deal with two pets having tasks at the same time. I also do not know what will happen if the user inputs overlapping availability windows. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with how I handled scheduling logic. I feel like that was the most complicated part of the project and satisfying to solve because everything else felt more tedious (primarily front end display, which is not my forte). 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would make it so the user can edit tasks and make the same task apply to multiple pets (like feeding all your pets at once). 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One takeaway is that it is important to plan out the design of your system and clearly layout your vision for the site. If you don't, then the AI will compromise your vision and values. In the end, I still designed most of the website structure and functionality - AI just handled most of the details and squashed bugs.
