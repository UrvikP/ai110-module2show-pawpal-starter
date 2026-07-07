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

Upon reaching phase 2, I noticed that Task class does not have the ability to mark a task as complete. I added this attribute in the task class.

Also it seems there should be a scheduler Class that is in Charge of making the Schedule. I had initially baked this right into the Owner class. I asked Claude to instead Create a new Scheduler class. I've taken out the priority class and made it a string set at the creation of a new task. I've opted to create a module that assigns each priority string a number, and the scheduler class will now gather all the data from an owner class and then order it based on the time and then by priority.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - I wanted to make sure the schedule was displayed in order from the start time.
    - The time it takes to do a task is factored in when creating another task, to avoid time conflicts.
        - Conflict resolution has been added, we don't want conflicting tasks in the list. Even if the pet name is the same or different, the time will always be compared to ensure no conflict occurs.
    - User driven feature were implemented to filter for things like "marked as complete" etc.
- How did you decide which constraints mattered most?
    - Logically, tasks need to be order by start time. We also need to factor in the duration time as well to avoid overlapping tasks.
    - When we generate a Schedule, we need to make sure that each schedule only generates a schedule for ONE Owner and it includes all pets that Owner owns. 
    - I haven't included a constraint to skip any tasks when the time has run out for them.
    


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    Sorting and filtering is all built into one method (build_plan).
    This is done because the filter options are limited in my project. I don't plan on adding any additional filters, so the parameters won't be changing. If i needed more filter, Claude AI does reommend creating a filters object.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
    I used AI to help me brainstorm, generate code for specific functions, and finally after confirming that the code works, highlighting specific methods/code blocks to see if it can be refactored. 
        - I told the AI about a problem relating to UI, specifically the generate schedule button, and asked it to change or add features like sorting by time or priority, then filtering by pet name or by task completion.
    - I've asked the AI to determine if certain methods can be refactored. It actually said no and didn't recommend that i change anything. It did offer another version, but that version, as it warned was highly unreadable and hard to debug, and I agreed so I didnt make the change.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    I did a good job of asking it for multiple different variations and explamantions for each variation. Each code had tradeoffs and based off of those tradeoffs, I made my decision on which route to go. In fact, I've made usre to ask for multiple variations for pretty much everything.
        - Code readablility is very important to me. Also making sure I'm not changing all my previous logic is crucial. I need to understand my code, otherwise I'm probably spending more time understanding the code than implementing minor changes here and there.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    Any changes I made, such a conflic resolution, filtering and sorting was testing. Any algorithm that was created and or changed was tested, either with an existing test or a new test developed to test the new feature. I specifically asked the AI to test each new algorithm. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Confidence level: 5
- What edge cases would you test next if you had more time?
    Overall I'm pretty confident that my scheduler works well. As for edge cases, I handled multiple owners, multiple pets, no pets, no tasks, daily task and weekly tasks, and dates.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I think the planning part was the most satisfying. I was satisfied with creating the UML diagram and the skeleton for the classes. Even though it changed alot throughout the course fo the project, It was atleast interesting to see all the changes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    - probably improve the UI more.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    Designing systems is challenging at the beginning because it is very hard to account for everything. Also the ammount of changes you'll notice as you begin implementing algorithms and then UI is substantial to me. AI absolutely helped to make sense of everything and not get lost, aswell as wire methods and algorithms to UI elements. It just turned what feels like a week long project into an 8 hour sprint. I can see why AI is so hpyed by many engineers.