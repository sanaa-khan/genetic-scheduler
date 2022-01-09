#####################################################################################################################
###         Hassan Shahzad & Sana Ali
###         CS-D
###         Artificial Intelligence (Project # 1)
###         FAST-NUCES
###         chhxnshah@gmail.com
#####################################################################################################################

#################################################### ASSUMPTIONS ####################################################

# A1: There are 2 time slots in a day: Morning and Noon (Hard Const 4: Exam must be held between 9am - 5pm )
# A2: Each exam will be of 3 hours
# A3: Morning Slot = 9am - 12pm
# A4: Evening Slot = 2pm - 5pm
# A5: It is possible that not all classrooms are used in a single day
# A6: We are assuming that one exam will be scheduled once only (NOT FOLLOWING THIS ANY MORE)
# A7: The higher the fitness score, the better the solution (Our goal is to maximize fitness value)
# A8: Any day with exams scheduled will have exam at both morning and noon

#####################################################################################################################


#################################################### LIBRARIES ######################################################

import collections
import csv
import random
from copy import deepcopy

from colorama import Fore, Back
from numpy import random
from numpy.random import randint

################################################### GLOBALS #########################################################

# Hard Const 7 : Total of 10 rooms

room_names = ['C301', 'C302', 'C303', 'C304', 'C305', 'C306', 'C307', 'C308', 'C309', 'C310']

# Hard Const 3 : No exams on weekends

total_days = ['Week 1 : Mon', 'Week 1 : Tue', 'Week 1 : Wed', 'Week 1 : Thu', 'Week 1 : Fri', 'Week 2 : Mon',
              'Week 2 : Tue', 'Week 2 : Wed', 'Week 2 : Thu', 'Week 2 : Fri', 'Week 3 : Mon', 'Week 3 : Tue',
              'Week 3 : Wed']

# Hard Const 5 : Each exam must have an invigilator.

classrooms = collections.namedtuple('classroom', 'room_name morning invig_morning noon invig_noon')


#####################################################################################################################
#################################################### CLASSES ########################################################
#####################################################################################################################


################################################# Student Data Class ################################################

# This class will basically contain the name of students alongwith the array containing the courses he studies

class StudentData:
    def __init__(self, name, courses):
        self.name = name
        self.courses = []
        self.courses.append(courses)

    def add_course(self, course):
        self.courses.append(course)

    def __repr__(self):  # return string representation so it can be printed
        output = "Name: " + self.name + "\t" + "Courses: " + str(self.courses) + "\n"
        return output


def add_student(student_list, name, cc):  # add a course for a specific student in the list

    for student in student_list:
        if student.name == name:
            if cc not in student.courses:  # To cater repeated value
                student.add_course(cc)
            return

    new_student = StudentData(name, cc)
    student_list.append(new_student)


################################################# Schedule Class #####################################################

# This class will basically act as a solution.It consists of days and a collection of room info, timee slots and
# teachers on invigilation duties. We have created a dictionary to store a collection corresponding each day of the week

class Schedule:
    def __init__(self, days=dict(), fitness=0):
        self.days = days
        self.fitness = fitness

        for day in total_days:
            self.days[day] = []


#####################################################################################################################
#################################################### FUNCTIONS ######################################################
#####################################################################################################################


#################################################### Loading Data ###################################################

def is_course_in_list(courses, code):
    for course in courses:
        if code == course[0]:
            return True

    return False


# This function loads each csv file into appropriate data types for future use.

def load_data():
    courses = []

    with open("data/courses.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # Loading courses
        for row in csv_reader:
            code_title = row[0], row[1]

            if not is_course_in_list(courses, code_title[0]):
                courses.append(code_title)

    # -------------------- #

    teacher = []

    with open("data/teachers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # Loading teachers
        for row in csv_reader:
            if len(row) > 0:
                name = row[0]
                teacher.append(name)

    # -------------------- #

    student_list = []
    with open("data/studentCourse.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # Reading students and their courses
        line = 0
        for row in csv_reader:
            if line != 0:
                name = row[1]
                cc = row[2]
                add_student(student_list, name, cc)
            line += 1

    return courses, teacher, student_list  # Returning all data


################################################# Utility Functions ##################################################

# Printing Functions

def print_custom_class(classes_list):
    for _class in classes_list:
        morning_paper = _class.morning.ljust(6)
        m_invigilator = _class.invig_morning.ljust(18)
        noon_paper = _class.noon.ljust(6)
        n_invigilator = _class.invig_noon.ljust(18)

        print(Back.CYAN + "   " + Fore.BLACK + _class.room_name + "  " + Back.RESET + Fore.RESET, sep='', end='')
        print(Back.GREEN + "  " + Fore.BLACK + morning_paper + "  " + Back.RESET + Fore.RESET, sep='', end='')
        print(Back.YELLOW + "  " + Fore.BLACK + m_invigilator + "  " + Back.RESET + Fore.RESET, sep='', end='')
        print(Back.GREEN + "  " + Fore.BLACK + noon_paper + "  " + Back.RESET + Fore.RESET, sep='', end='')
        print(Back.YELLOW + "  " + Fore.BLACK + n_invigilator + "  " + Back.RESET + Fore.RESET)


def print_custom_schedule(schedule):
    for day in schedule.days:
        if len(schedule.days[day]) > 0:
            print()
            print(Back.BLACK + "                                                                         " + Back.RESET)
            print(
                Back.BLACK + Fore.WHITE + "                               " + day + "                              " + Fore.RESET + Back.RESET)
            print(Back.BLACK + "                                                                         " + Back.RESET)
            print_custom_class(schedule.days[day])


def print_classes_list(classes_list):
    for _class in classes_list:
        print(_class)


def print_schedule(schedule):
    for day in schedule.days:
        if len(schedule.days[day]) > 0:
            print("\nDay: ", day)
            print_classes_list(schedule.days[day])


def print_population(population):
    count = 1
    for schedule in population:

        print("Schedule #", count, "\n")
        print("Fitness: ", schedule.fitness)
        for day in schedule.days:
            print("\nDay: ", day, "\n\n")
            print_classes_list(schedule.days[day])
            print("\n")

        count += 1


############################################# Generating Population ##################################################

# This function is used to generate set of random solutions.

def generate_population(population_size, courses, teachers):
    new_pop = []

    for i in range(0, population_size):
        schedule = Schedule(dict())

        for day in total_days:

            visited_indexes = []
            total_classrooms = random.randint(0, len(
                room_names))  # Classrooms = room_name, morning, invig_morning, noon, invig_noon

            for j in range(total_classrooms):

                index = random.randint(0, len(room_names))  # Generating that number of classrooms

                while index in visited_indexes:
                    index = random.randint(0, len(room_names))

                room = room_names[index]
                visited_indexes.append(index)

                index1 = random.randint(0, len(courses))  # Randomly picking morning course
                m_course = courses[index1][0]

                index2 = random.randint(0, len(teachers))  # Randomly picking invigilator for morning
                m_invig = teachers[index2]

                index3 = random.randint(0, len(courses))  # Randomly picking noon course
                n_course = courses[index3][0]

                index4 = random.randint(0, len(teachers))  # Randomly picking invigilator for noon
                n_invig = teachers[index4]

                # noinspection PyArgumentList
                schedule.days[day].append(
                    classrooms(
                        room_name=room,
                        morning=m_course,
                        invig_morning=m_invig,
                        noon=n_course,
                        invig_noon=n_invig
                    )
                )

        new_pop.append(schedule)

    return new_pop


################################################# Constraints Check ##################################################

def hconstraint_all_courses(schedule, courses):  # Hard Const 1 = Exam scheduled for every course

    bool_check = False

    exam_list = []
    total_exams = 0

    for day in schedule.days:  # Getting list of all exams in the schedule week
        class_list = schedule.days[day]

        for _class in class_list:  # Examining every classroom assigned
            m_exam = _class.morning
            n_exam = _class.noon
            total_exams += 2

            if m_exam not in exam_list:
                exam_list.append(m_exam)

            if n_exam not in exam_list:
                exam_list.append(n_exam)

    exam_codes = []  # List of all exams

    for course in courses:
        code = course[0]
        exam_codes.append(code)  # Gets list of all exam codes of all courses

    missing = 0
    for code in exam_codes:
        if code not in exam_list:  # Comparing the two lists
            missing += 1  # Number of courses not listed

    if missing == 0:  # If the constraint is satisfied completely
        bool_check = True

    num = (1 / (1 + missing))

    return num, bool_check


def hconstraint_three_courses(course_allocation):  # Hard Const 2 = Minimum 3 courses per student

    for student in course_allocation:
        if len(student.courses) < 3:  # If a student is registered in less than 3 courses
            return False

    return True


def hconstraint_clashing_exams(schedule, course_allocation):  # Hard Const 2.1 : Student has 1 exam at a time

    exam_list = []

    for day in schedule.days:  # getting list of all exams in this schedule
        classes_list = schedule.days[day]

        for _class in classes_list:  # Storing all exams for that day
            exam_list.append(_class.morning)
            exam_list.append(_class.noon)

    exam_counts = dict(collections.Counter(exam_list))

    clashes = 0
    student_names_clashes = []
    bool_check = False

    for day in schedule.days:  # Getting list of classrooms for every day
        classes_list = schedule.days[day]

        morning_list = []
        noon_list = []

        for _class in classes_list:  # Getting lists of all exams on morning and noon
            morning_list.append(_class.morning)
            noon_list.append(_class.noon)

        for student in course_allocation:  # Examining all students and their allocated courses
            course_list = student.courses
            name = student.name

            clash_flag = False  # Checking if record clashes for a student

            count = 0
            for course in morning_list:
                if course in course_list:
                    if course in exam_counts.keys():
                        if exam_counts[course] == 1:  # exam only at this specific time
                            count += 1  # Counting clashes in morning for a student

            if name not in student_names_clashes:
                if count > 1:
                    clash_flag = True
                    clashes += 1
                    student_names_clashes.append(name)

            count = 0
            for course in noon_list:
                if course in course_list:
                    if course in exam_counts.keys():
                        if exam_counts[course] == 1:
                            count += 1

            if name not in student_names_clashes:
                if count > 1 and not clash_flag:
                    clashes += 1  # Counting clashes in evening for a student
                    student_names_clashes.append(name)

    if clashes == 0:  # If the constraint is satisfied completely
        bool_check = True

    num = (1 / (1 + clashes))

    return num, bool_check


def hconstraint_teachers_sametime(schedule):  # Hard Const 5.1 : No teacher clashes at the same time

    clashes = 0
    bool_check = False

    for day in schedule.days:
        classes_list = schedule.days[day]
        morning_list = []
        noon_list = []

        for _class in classes_list:  # Getting lists of all teachers on morning and noon
            morning_list.append(_class.invig_morning)
            noon_list.append(_class.invig_noon)

        dup_count_morning = dict(collections.Counter(morning_list))  # Getting the number of duplicate entries
        dup_count_noon = dict(collections.Counter(noon_list))

        for value in dup_count_morning.values():
            if value > 1:
                clashes += 1  # Calculating the number of clashes

        for value in dup_count_noon.values():
            if value > 1:
                clashes += 1

    if clashes == 0:  # If the constraint is satisfied completely
        bool_check = True

    num = (1 / (1 + clashes))

    return num, bool_check


def hconstraint_teacher_samerow(schedule):  # Hard Const 6 : No teacher has duties in a row

    consecutive = 0
    bool_check = False
    for day in schedule.days:
        classes_list = schedule.days[day]
        morning_list = []
        noon_list = []

        for _class in classes_list:  # Getting lists of all teachers on morning and noon
            morning_list.append(_class.invig_morning)
            noon_list.append(_class.invig_noon)

        for teacher in morning_list:
            if teacher in noon_list:
                consecutive += 1  # Calculating the number of consecutive duties

    if consecutive == 0:  # If the contraint is satisfied completely
        bool_check = True

    num = (1 / (1 + consecutive))

    return num, bool_check


def hconstraint_course_scheduled_once(schedule):  # Hard Const 8: One course must be scheduled once only

    repeated = 0
    scheduled = []
    bool_check = False

    for day in schedule.days:
        classes_list = schedule.days[day]

        for _class in classes_list:  # Getting lists of all courses on morning and noon
            scheduled.append(_class.morning)
            scheduled.append(_class.noon)

    dup_counts = dict(collections.Counter(scheduled))  # Counting the courses scheduled more than once

    for value in dup_counts.values():
        if value > 3:
            repeated += 1

    if repeated == 0:  # If the constraint is satisfied completely
        bool_check = True

    num = (1 / (1 + repeated))

    return num, bool_check


def sconstraint_less_days(schedule):  # Soft Const 3: Schedule in less days

    no_days = 0

    for day in schedule.days:
        classes_list = schedule.days[day]  # Getting schedule for each day

        if not classes_list:  # Checks if nothing is scheduled
            no_days += 1

    n = len(total_days) - no_days
    num = (1 / (1 + n))

    return num, no_days  # If empty days are more = Solution is better


def sconstraint_mg_before(schedule, course_allocation):  # Soft Const 4: MG courses scheduled before CS courses

    student_list = []
    bool_check = False

    for student in course_allocation:  # For every student
        mg_flag = False
        cs_flag = False

        for course in student.courses:  # Checks if a student opts both CS and MG courses
            if 'MG' in course:
                mg_flag = True
            if 'CS' in course:
                cs_flag = True

        if mg_flag and cs_flag:
            student_list.append(student)  # List of students meeting the condition

    student_names = []
    wrong_order = 0

    for i in range(0, len(student_list) - 1):  # For every student
        student = student_list[i]
        cs_flag = False

        for day in schedule.days:  # Checks schedule of all 5 days for each student
            classes_list = schedule.days[day]
            exam_list = []

            for _class in classes_list:  # Storing all exams for that day
                exam_list.append(_class.morning)
                exam_list.append(_class.noon)

            for course in student.courses:
                if 'CS' in course:
                    if course in exam_list:
                        cs_flag = True  # Checks if CS couse of student comes before MG

                elif 'MG' in course:
                    if course in exam_list:
                        if cs_flag:  # If MG comes after CS
                            if student.name not in student_names:
                                student_names.append(student.name)
                                wrong_order += 1
                            i += 1

    if wrong_order == 0:  # If the constraint is satisfied completely
        bool_check = True

    num = (1 / (1 + wrong_order))

    return num, bool_check


def constraints_satisfied_check(schedule, courses, course_allocation):
    hc1, hb1 = hconstraint_all_courses(schedule, courses)
    hc2, hb2 = hconstraint_clashing_exams(schedule, course_allocation)
    hc3, hb3 = hconstraint_teachers_sametime(schedule)
    hc4, hb4 = hconstraint_teacher_samerow(schedule)
    hc5, hb5 = hconstraint_course_scheduled_once(schedule)
    _, sb2 = sconstraint_less_days(schedule)
    sc3, sb3 = sconstraint_mg_before(schedule, course_allocation)

    # all hard constraints satisfied
    if hb1 and hb2 and hb3 and hb4:
        # at least one soft constraint (2 already satisfied by default)
        if sb2 > 0 or sb3:
            return True

    return False


def print_check():
    print(Back.BLACK + "                                                                         " + Back.RESET)
    print(
        Back.BLACK + Fore.WHITE + "                             " + "HARD CONSTRAINTS" + "                            " + Fore.RESET + Back.RESET)
    print(Back.BLACK + "                                                                         " + Back.RESET)

    h1 = "1: Exam is scheduled for each course = " + '\u2705' + '\u2705'
    h2 = "2: Student cannot give more than one exam at a time = " + '\u2705' + '\u2705'
    h3 = "3: Teacher invigilates one exam at a time = " + '\u2705' + '\u2705'
    h4 = "4: Teacher invigilates one exam in a row = " + '\u2705' + '\u2705'
    h5 = "5: Student is enrolled in atleast 3 courses = " + '\u2705' + '\u2705'
    h6 = "6: Exam wont be held on weekends = " + '\u2705' + '\u2705'
    h7 = "7: Exam must be invigilated by a teacher = " + '\u2705' + '\u2705'
    h8 = "8: Use at max 10 classrooms = " + '\u2705' + '\u2705'

    hc1 = h1.ljust(58)
    hc2 = h2.ljust(58)
    hc3 = h3.ljust(58)
    hc4 = h4.ljust(58)
    hc5 = h5.ljust(58)
    hc6 = h6.ljust(58)
    hc7 = h7.ljust(58)
    hc8 = h8.ljust(58)

    print(Back.RED + Fore.WHITE + "  " + hc1 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc2 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc3 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc4 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc5 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc6 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc7 + "          " + Fore.RESET + Back.RESET)
    print(Back.RED + Fore.WHITE + "  " + hc8 + "          " + Fore.RESET + Back.RESET)

    print()
    print(Back.BLACK + "                                                                         " + Back.RESET)
    print(
        Back.BLACK + Fore.WHITE + "                             " + "SOFT CONSTRAINTS" + "                            " + Fore.RESET + Back.RESET)
    print(Back.BLACK + "                                                                         " + Back.RESET)

    s1 = "1: Break on Friday from 1-2pm = " + '\u2705' + '\u2705'
    s2 = "2: Student should not give more than 1 exam consecutively = " + '\u2705' + '\u2705'
    s3 = "3: MG Course scheduled before CS Course = " + '\u2705' + '\u2705'
    s4 = "4: Exam is scheduled in less days = " + '\u2705' + '\u2705'
    s5 = "5: Almost equal number of invigilation duties = " + '\u2705' + '\u2705'

    sc1 = h1.ljust(60)
    sc2 = h2.ljust(60)
    sc3 = h3.ljust(60)
    sc4 = h4.ljust(60)
    sc5 = h5.ljust(60)

    print(Back.BLUE + Fore.BLACK + "  " + sc1 + "        " + Fore.RESET + Back.RESET)
    print(Back.BLUE + Fore.BLACK + "  " + sc2 + "        " + Fore.RESET + Back.RESET)
    print(Back.BLUE + Fore.BLACK + "  " + sc3 + "        " + Fore.RESET + Back.RESET)
    print(Back.BLUE + Fore.BLACK + "  " + sc4 + "        " + Fore.RESET + Back.RESET)
    print(Back.BLUE + Fore.BLACK + "  " + sc5 + "        " + Fore.RESET + Back.RESET)


def constraints_satisfied_print(schedule, courses, course_allocation):
    hc1, hb1 = hconstraint_all_courses(schedule, courses)
    hc2, hb2 = hconstraint_clashing_exams(schedule, course_allocation)
    hc3, hb3 = hconstraint_teachers_sametime(schedule)
    hc4, hb4 = hconstraint_teacher_samerow(schedule)
    hc5, hb5 = hconstraint_course_scheduled_once(schedule)
    sc2, sc_days = sconstraint_less_days(schedule)
    sc3, sb3 = sconstraint_mg_before(schedule, course_allocation)

    print("\n---------------------------------\n")
    print("Hard constraints: \n")

    print("hc1 = ", hc1, " hc2 = ", hc2, " hc3 = ", hc3, " hc4 = ", hc4, "hc5 = ", hc5, " sc2 = ", sc2, " sc3 = ", sc3)

    print("An exam will be scheduled for each course: ", end='')

    if hb1:
        print('\u2705')
    else:
        print('\u2716')

    print("A student cannot give more than 1 exam at a time: ", end='')

    if hb2:
        print('\u2705')
    else:
        print('\u2716')

    print("A teacher cannot invigilate two exams at the same time: ", end='')
    if hb3:
        print('\u2705')
    else:
        print('\u2716')

    print("A teacher cannot invigilate two exams in a row: ", end='')
    if hb4:
        print('\u2705')
    else:
        print('\u2716')

    print("\n\nSoft constraints: \n")

    print("A student shall not give more than 1 exam consecutively: " + '\u2705')

    print(
        "If a student is enrolled in a MG course and a CS course, it is preferred that their MG course exam be held "
        "before their CS course exam: ",
        end='')

    if sb3:
        print('\u2705')
    else:
        print('\u2716')

    print("Schedule in less days: ", end='')

    if sc_days > 0:
        print('\u2705')
    else:
        print('\u2716')
    print()
    print()


#####################################################################################################################
################################################# UTILITIES FOR GA ##################################################
#####################################################################################################################

def calculate_fitness(population, courses, course_allocation):
    for schedule in population:  # For each schedule in a population
        hc1, hb1 = hconstraint_all_courses(schedule, courses)
        hc2, hb2 = hconstraint_clashing_exams(schedule, course_allocation)
        hc3, hb3 = hconstraint_teachers_sametime(schedule)
        hc4, hb4 = hconstraint_teacher_samerow(schedule)
        hc5, hb5 = hconstraint_course_scheduled_once(schedule)
        sc2, empty_days = sconstraint_less_days(schedule)
        sc3, sb3 = sconstraint_mg_before(schedule, course_allocation)

        fitness = hc1 + hc2 + hc3 + hc4 + sc2 + sc3  # Calculating the fitness of the schedule
        schedule.fitness = fitness  # Adding the fitness to the class

        if empty_days > 7:
            schedule.fitness -= 2

    return population


def get_fitness(schedule):  # Returning fitness
    return schedule.fitness


def two_fittest_schedules(population):  # Selecting two fittest solutions (schedules)
    pop = deepcopy(population)
    pop.sort(key=get_fitness, reverse=True)  # Sorts in descending order
    return pop[0], pop[1]


def roulette_wheel(population):  # Roulette Wheel Selection

    # parents = []
    # total_fitness = 0
    #
    # for schedule in population:
    #     total_fitness += schedule.fitness
    #
    # highest, second_highest = two_fittest_schedules(population)  # Getting two fittest solutions
    # parents.append(highest)
    # parents.append(second_highest)
    # fitness_sum = 0
    #
    # while len(parents) < len(population):
    #
    #     individual = random.randint(0, len(population))  # Getting a random index
    #     fitness_sum += population[individual].fitness
    #     if fitness_sum >= total_fitness:  # Individual chosen based on its probability
    #         if population[individual] not in parents:
    #             parents.append(deepcopy(population[individual]))
    #
    # return parents

    max_ = sum([schedule.fitness for schedule in population])
    pick = random.uniform(0, max_)
    current = 0

    for chromosome in population:
        current += chromosome.fitness
        if current > pick:
            return chromosome


def mix_days(parent_a, parent_b):  # Generating new schedule

    no_days_to_mix = randint(1, len(total_days))  # Random crossover point
    child1 = Schedule()
    child2 = deepcopy(child1)

    i = 0
    for day in total_days:

        if i < no_days_to_mix:  # Taking that # of days from first parent
            classes_list_a = parent_a.days[day]
            classes_list_b = parent_b.days[day]

            child1.days[day] = deepcopy(classes_list_a)
            child2.days[day] = deepcopy(classes_list_b)

        else:  # Taking rest of days from second parent
            classes_list_a = parent_a.days[day]
            classes_list_b = parent_b.days[day]

            child1.days[day] = deepcopy(classes_list_b)
            child2.days[day] = deepcopy(classes_list_a)

        i += 1

    return child1, child2


def mutate_schedule(schedule, mutation_probability, courses, teachers):  # Applying mutation on chromosomes

    if randint(0, 100) <= mutation_probability * 100:  # Checking prob for mutation
        random_days = randint(0, len(total_days))  # Selecting random no of days to change

        for i in range(0, random_days):
            # choosing a random day
            idx = randint(0, len(total_days))
            day = total_days[idx]

            classes_list = schedule.days[day]

            # if it had assigned classes/exams
            if len(classes_list) > 0:
                if randint(0, 2) == 1:
                    for j in range(0, len(classes_list)):  # Will change one class at a time

                        if randint(0, 2) == 1:  # 50% probabilty for mutation
                            index = random.randint(0, len(courses))  # Randomly replacing course
                            morning = courses[index][0]

                            index = random.randint(0, len(teachers))  # Randomly replacing invigilator
                            invig_morning = teachers[index]

                            index = random.randint(0, len(courses))  # Randomly replacing course
                            noon = courses[index][0]

                            index = random.randint(0, len(teachers))  # Randomly replacing invigilator
                            invig_noon = teachers[index]

                            # Updating the values
                            classes_list[j] = classes_list[j]._replace(morning=morning, invig_morning=invig_morning)
                            classes_list[j] = classes_list[j]._replace(noon=noon, invig_noon=invig_noon)
                else:
                    classes_list.clear()

            # if that day was empty, then assign it some classes/exams
            else:
                visited_indexes = []
                total_classrooms = random.randint(0,
                                                  5)  # Classrooms = room_name, morning, invig_morning, noon, invig_noon

                for j in range(total_classrooms):

                    index = random.randint(0, 9)  # Generating that number of classrooms

                    while index in visited_indexes:
                        index = random.randint(0, 9)

                    room = room_names[index]
                    visited_indexes.append(index)

                    index = random.randint(0, len(courses))  # Randomly picking morning course
                    m_course = courses[index][0]

                    index = random.randint(0, len(teachers))  # Randomly picking invigilator for morning
                    m_invig = teachers[index]

                    index = random.randint(0, len(courses))  # Randomly picking noon course
                    n_course = courses[index][0]

                    index = random.randint(0, len(teachers))  # Randomly picking invigilator for noon
                    n_invig = teachers[index]

                    classes_list.append(
                        classrooms(
                            room_name=room,
                            morning=m_course,
                            invig_morning=m_invig,
                            noon=n_course,
                            invig_noon=n_invig
                        )
                    )

    return schedule  # Returning the mutated schedule


def apply_crossover(population, crossover_probability):  # Applying

    crossovered_population = []

    # equal length crossover
    while len(crossovered_population) < len(population):
        if randint(0, 100) <= crossover_probability * 100:
            parent_a = deepcopy(roulette_wheel(population))
            parent_b = deepcopy(roulette_wheel(population))

            child1, child2 = mix_days(parent_a, parent_b)

            crossovered_population.append(deepcopy(child1))
            crossovered_population.append(deepcopy(child2))

    return crossovered_population


def apply_mutation(population, mutation_probability, courses, teachers):
    mutated_population = []

    for schedule in population:
        s = mutate_schedule(schedule, mutation_probability, courses, teachers)
        mutated_population.append(deepcopy(s))

    return mutated_population


################################################# Genetic Algorithm ##################################################

# This is the main implementation of the Genetic Algorithm

def genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, courses, teachers,
                 course_allocation):
    if not hconstraint_three_courses(course_allocation):
        print("Data is flawed. Every student must have at least 3 courses allocated. Terminating program :(")
        return None

    best_solution = None

    # Generating a list of schedules
    population = [generate_population(population_size, courses, teachers)]

    # For seeing if algorithm is unable to optimise further
    stagnant = 0
    reset_count = 0
    solutions_list = []
    prev_best = None

    for i in range(max_generations):

        # Evaluating fitness
        pop = calculate_fitness(population[0], courses, course_allocation)

        # Applying crossover
        crossover_population = apply_crossover(pop, crossover_probability)
        calculate_fitness(crossover_population, courses, course_allocation)

        # Applying mutation
        mutated_population = apply_mutation(crossover_population, mutation_probability, courses, teachers)
        calculate_fitness(mutated_population, courses, course_allocation)

        # Finding fittest candidate
        schedule1, _ = two_fittest_schedules(mutated_population)

        if best_solution is None:
            stagnant = 0
            best_solution = deepcopy(schedule1)

        elif schedule1.fitness > best_solution.fitness:
            stagnant = 0
            best_solution = deepcopy(schedule1)

        if best_solution.fitness == prev_best:
            stagnant += 1

        prev_best = deepcopy(best_solution.fitness)

        if constraints_satisfied_check(best_solution, courses, course_allocation):
            constraints_satisfied_print(best_solution, courses, course_allocation)
            print()
            print(Back.BLACK + "                                                                         " + Back.RESET)
            print(
                Back.BLACK + Fore.WHITE + "                             SOLUTION FOUND!!!!                          " + Fore.RESET + Back.RESET)
            print(Back.BLACK + "                                                                         " + Back.RESET)
            print()
            return best_solution

        # no further optimisation for this # of generations
        if stagnant == 50:
            if reset_count < 3:
                print(
                    "\n-------------------\nAlgorithm is unable to optimise further. Starting over with a new random population.\n-------------------\n")
                solutions_list.append(deepcopy(best_solution))

                i = 0
                stagnant = 0
                reset_count += 1

                pop = generate_population(population_size, courses, teachers)
                best_solution = None
                population.clear()
                population.append(pop)
                continue

            else:
                print(
                    "\nAlgorithm unable to optimise further. Terminating program and returning best solution upto now.\n")
                best, _ = two_fittest_schedules(solutions_list)
                return best

        else:
            # generating new population
            population.clear()
            population.append(mutated_population)

        if i % 25 == 0:
            print("Current generation so far: ", i)
            print("Best solution so far: \nFitness: ", best_solution.fitness)
            print_schedule(best_solution)
            constraints_satisfied_print(best_solution, courses, course_allocation)

        print(i, "- Fitness of best solution: ", best_solution.fitness, "\t( Fitness of local best solution: ",
              schedule1.fitness, ")", "\t( Stagnation: ", stagnant, ")")

    return best_solution


#####################################################################################################################
################################################# Main Implementation ###############################################
#####################################################################################################################


# The main entry point for this module
def main():
    courses, teachers, course_allocation = load_data()

    population_size = random.randint(50, 200)  # number of solutions in a population
    max_generations = random.randint(100, 1000)  # how long to iterate

    crossover_probability = 1
    mutation_probability = 0.2

    print('\n\n--- Generated Parameters -----')
    print('Population size......: {}'.format(population_size))
    print('Number of generations: {}'.format(max_generations))
    print('Crossover probability: {}'.format(crossover_probability))
    print('Mutation probability: {}'.format(mutation_probability))

    res = genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, courses, teachers,
                       course_allocation)

    print_custom_schedule(res)
    print_check()
    print()


# Tell python to run main method
if __name__ == "__main__":
    main()
