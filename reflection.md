# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my UML Design, I wanted to focus on classes that actively provide information to a specific pet and pet owner. I've considered things like:
    - What if the Owner has multiple pets
        - For each Pet, what tasks need to be done
            - For each task, is there a time limit of when the task needs to be done by
            - Tasks should be ordered in terms of time limit.
            - Examples of tasks include: scheduling a time for a walk, feeding time, and being able to see the entire list of tasks they added for the specific pet.
    
    In conclusion: I have the following classes.
    - Owner class: theres are methods for the following:
        - Set owner name.
        - Initialize a list of Pets they own
        - Add a Pet (this will initialize a Pet Object)
        - Possibly include a daily plan function that allows the list of tasks to be sorted by time or priority.
    - Pet class:
        - I want the name of the pet intialized.
        - Type of pet: for example Dog, Cat, Bird, etc
    - Task class:
        - Initialize a task by: Time start, Description, duration, priority
        - Every Pet has a list of Tasks (Leaning towards a dictionary)
            - Each task needs to be identified by time.
            - Every task has a priority: High, Medium, Low
            - Every task has an explanation
            - Every task has a duration for example, "10min"
    - Priority class:
        - Sets the priority of a Task: High, Medium, Low



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

One change that was made was changing the Priority element into a class. This was done by the AI and I think it looks better so I decided to keep it.

    - When I had the create a Python Class skeleton, I notice the set_name function in the Owner class. I took a look in app.py and see that there's no directive or reason to have a function that allows the user to change their name. So i opted to delete this function. I made sure to ask Claude why it was written in the first place, just to be safe and it pretty much agreed that it was redundant as the name variable is public so it can easily be rename to something else for example: Owner.name = "New Name Here"
        - This change was also made in the UML draft by removing +set_name from the draft.

Upon asking Claude AI to review the UML diagram along with pawpal_system.py, it mentioned that while Owner can refer to pet and pet can refer to list, a list doesn't know which pet it belongs to, a pet doesn't know who it's owner is and so when we sort tasks, this inability to back-reference will cause problems especially for sorting daily tasks.
    - Another mention was that duration was actually a string. It recommended that it be a Int to sum durations and compare available time.
    - I also changed the Priority class to assign numeric values, this way its easier to sort by Priority.
    - The dialy_plan method will sort the tasks by time with a secondary preference to prioprity just in case an owner has mutliple things they want to do and alotted that same start time.

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
