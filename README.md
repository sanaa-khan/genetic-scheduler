# Exam Schedule Generator using Genetic Algorithm

## Requirements
- Use any kind of crossover
- Choose any justifiable rate of mutation
- Use roulette wheel selection for selecting potentially useful solutions for recombination

The success of the solution is estimated on fulfillment of given constraints and criteria. Results of testing the algorithm show that all hard constraints are satisfied, while additional criteria is optimised to a certain extent.

## Constraints
There is a set of constraints that needs to be fulfilled.

### Hard Constraints
- An exam will be scheduled for each course.
- A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
- Exam will not be held on weekends.
- Each exam must be held between 9 am and 5 pm
- Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same time.
- A teacher cannot invigilate two exams in a row

**The above-mentioned constraints must be satisfied.**

### Soft Constraints
- All students and teachers shall be given a break on Friday from 1-2.
- A student shall not give more than 1 exam consecutively.
- If a student is enrolled in a MG course and a CS course, it is preferred that their MG course exam be held before their CS course exam. 
- Two hours of break in the week such that at least half the faculty is free in one slot and the rest of the faculty is free in the other slot so the faculty meetings shall be held in parts as they are now.

## Input & Output
Input data for each exam are teachers’ names, students’, exam duration, courses (course codes), and list of allowed classrooms.

Output data are classroom and starting time for each exam along with course code and invigilating teacher. Time is determined by day (Monday to Friday) and start hour of the exam.

- Output will be a chromosome which satisfies all hard constraints and soft constraints at least three. (as much as you can)
- You have to display a list of all hard and soft constraints which are fulfilled in the output.
- Don’t forget to show fitness values at each iteration.

## Credits
This project was done with equal contribution from my group partner [Hassan Shahzad](https://github.com/HxnDev) and I.

## Contact Me
<p align="center">
	<a href="mailto:sanakahnn@gmail.com"><img src="https://img.icons8.com/bubbles/50/000000/gmail.png" alt="Gmail"/></a>
	<a href="https://github.com/sanaa-khan"><img src="https://img.icons8.com/bubbles/50/000000/github.png" alt="GitHub"/></a>
	<a href="https://www.linkedin.com/in/sana-khan-95a9771b3/"><img src="https://img.icons8.com/bubbles/50/000000/linkedin.png" alt="LinkedIn"/></a>
	
</p>
