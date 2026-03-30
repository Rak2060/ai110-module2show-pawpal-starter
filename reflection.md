# PawPal+ Project Reflection

## 1. System Design
Three core actions user should be able to perform:
    i) Make a pet profile with all its information
    ii) Schedule an evening walk in the nearby park
    iii) View today's tasks related to each pet

Objects needed for system:
    i) User ID
        (attributes: name, email, password, pet_list[] ; methods: createProfile(), editProfile())
    ii) Pet Class
        (attributes: petId, name, breed, physicalDetails (dictionary) ; methods: editData(), updateMedHistory(), summarizeData())
    iii) Task Class
        (attributes: taskId, petId, timeRequired ; methods: createTask(), editTask(), isCompleted())
    iv) Reminder Class
        (attributes: taskId, petId, reminderId, time, frequency, status ; methods: sendReminder(), createReminder(), editReminder(), snooze(), checkAvailaility())


**a. Initial design**

- Briefly describe your initial UML design.
    I defined four classes namely - User, Pet, Task and Reminder - to manage the basic attributes for each class. Like an ID for each class and initial methods to create, edit and update the attributes.
- What classes did you include, and what responsibilities did you assign to each?
    In User class, I defined name, email, password attributes. Then a list to keep track of how many pets owner has. Ths class will basically decide how the user interprets theirside of app. In Pet class, I defined its Id, name, breed and ther specific details. The methods in this class can edit and update the attributes and export all data as well for each pet. In Task Class, there are basic attributes defined for task realted to each pet, strategizing time needed for each and then the methods can access these attributes to edit or update them. Reminder Class has attributes to create, edit and update status for each task and methods are defined to sned reminders and snooze them. This class also chceks for availability of user and then schedules the task with a differnt method

**b. Design changes**

- Did your design change during implementation? - Yes, a bit
- If yes, describe at least one change and why you made it.
Added overlap of task prevention methodology, which prevents scheduling conflicts, that is important for a satisfactory scheduling experience to user.

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
