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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
