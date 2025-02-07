from itertools import chain



class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_in_progress = []
        self.finished_courses = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise TypeError("Можно оценивать только лекторов")
        if course not in self.courses_in_progress:
            raise ValueError(f"Студент {self.name} не изучает курс '{course}'")
        if course not in lecturer.courses_attached:
            raise ValueError(f"Лектор {lecturer.name} не ведет курс '{course}'")
        if not isinstance(grade, (int, float)) or not (1 <= grade <= 10):
            raise ValueError("Оценка должна быть числом от 1 до 10")

        lecturer.grades.setdefault(course, []).append(grade)

    def __str__(self):
        avg_grade = self.calculate_avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')

    def calculate_avg_grade(self):
        all_grades = list(chain.from_iterable(self.grades.values()))
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_avg_grade() < other.calculate_avg_grade()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'



class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self.calculate_avg_grade()
        return super().__str__() + f'\nСредняя оценка за лекции: {avg_grade}'

    def calculate_avg_grade(self):
        if not self.grades:
            return 0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return round(total / count, 1)

    def __lt__(self, other):
        return self.calculate_avg_grade() < other.calculate_avg_grade()

    def __gt__(self, other):
        return self.calculate_avg_grade() > other.calculate_avg_grade()


    def __le__(self, other):
        return self.calculate_avg_grade() <= other.calculate_avg_grade()

    def __ge__(self, other):
        return self.calculate_avg_grade() >= other.calculate_avg_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class GradeCalculator:
    @staticmethod
    def calculate_avg_grade(people, course, grade_type="grades"):
        """
        Рассчитывает среднюю оценку по курсу для списка людей.

        :param people: Список объектов (например, студентов) с атрибутами оценок.
        :param course: Название курса, для которого рассчитывается средняя оценка.
        :param grade_type: Тип оценок (по умолчанию "grades").
        :return: Средняя оценка, округленная до одного знака после запятой.
        """
        if not people:
            return 0  # Если список людей пуст, возвращаем 0

        total = 0
        count = 0

        for person in people:
            grades = getattr(person, grade_type, {}).get(course, [])
            if grades:  # Проверяем, есть ли оценки по курсу
                total += sum(grades)
                count += len(grades)

        return round(total / count, 1) if count else 0

# Создаем экземпляры классов
lecturer_1 = Lecturer('Ivan', 'Ivanov')
lecturer_1.courses_attached.append('Python')

lecturer_2 = Lecturer('Sergey', 'Petrov')
lecturer_2.courses_attached.append('Git')

reviewer_1 = Reviewer('Jon', 'Smit')
reviewer_1.courses_attached.append('Python')

reviewer_2 = Reviewer('Anna', 'Ivanova')
reviewer_2.courses_attached.append('Git')

student_1= Student('Roy', 'Eman')
student_1.courses_in_progress.append('Python')
student_1.finished_courses.append('Введение в программирование')

student_2 = Student('Ron', 'Wuizli')
student_2.courses_in_progress.append('Git')
student_2.finished_courses.append('Введение в программирование')

# Выставляем оценки
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_2.rate_hw(student_2, 'Git', 8)
reviewer_2.rate_hw(student_2, 'Git', 7)

student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Python', 9)
student_2.rate_lecture(lecturer_2, 'Git', 8)
student_2.rate_lecture(lecturer_2, 'Git', 7)

# Выводим информацию
print(lecturer_1)
print(lecturer_2)
print(reviewer_1)
print(reviewer_2)
print(student_1)
print(student_2)

# Сравниваем студентов и лекторов
print("lecturer_2 > lecturer_1 is", lecturer_2 > lecturer_1)
print("lecturer_2 < lecturer_1 is",lecturer_2 < lecturer_1)


# Подсчет средней оценки за домашние задания и лекции
print(GradeCalculator.calculate_avg_grade([student_1, student_2], 'Python'))
print(GradeCalculator.calculate_avg_grade([lecturer_1, lecturer_2], 'Python'))

