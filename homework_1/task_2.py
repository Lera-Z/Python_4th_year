import random


class Animal:
    def __init__(self, age, color, fav_food, weight):
        self.age = age
        self.color = color
        self.fav_food = fav_food
        self.weight = weight

    def eat(self):
        self.weight += 1


class Insect:
    def __init__(self, size, n_legs):
        self.size = size
        self.num_of_legs = n_legs

    def eat(self):
        self.size += 1


class Dog(Animal):
    def __init__(self, age, color, fav_food, weight):
        super().__init__(age, color, fav_food, weight)  #полиморфизм - задаем конкретные аттрибуты для собаки только у собаки
        self.wags_tail = True
        self.hates_cats = True

    def saw_cat(self):         # и делаем свой уникальный метод собаке
        return 'Woof-woof-woof!'


class Sparrow(Animal):
    def __init__(self, age, color, fav_food, weight):
        super().__init__(age, color, fav_food, weight)  # полиморфизм - задаем конкретные аттрибуты для воробья
        self.can_fly = True
        self.height_flight = 40
        self.builds_nest = True


class Fox(Dog):
    def __init__(self, age, color, fav_food, weight):
        super().__init__(age, color, fav_food, weight)  # полиморфизм - задаем конкретные аттрибуты для воробья
        self.color = 'red'
        self.cunning = 100500
        self.is_friendly = False


class Turtle(Animal):
    def __init__(self, age, color, fav_food, weight):
        super().__init__(age, color, fav_food, weight) # задаем конкретные аттрибуты для черепахи
        self.speed = 1
        self.vegetarian = True


class Ladybug(Insect):
    def __init__(self, size, n_legs):
        super().__init__(size, n_legs)      # задаем конкретные аттрибуты для божьей коровки
        self.is_nice = True
        self.brings_bread = True
        self.drinks_blood = False

    def bring_me_bread(self):            # уникальный метод для божьей коровки
        f = random.choice([0,1,2,3,4])
        if f == 0:
            return 'Sorry, but not today'
        else:
            return 'Here is your {} loaf(s) of bread'.format(f)


'''
В данном случае полиморфизм может пригодиться, например, при составлении электронного справочника о животных - общие
для всех животных поля и методы заданы в классе-родителе, а потомки получают собственные, особенные для них методы
'''
#
# bug = Ladybug(5, 4)
# print(bug.bring_me_bread())

anim = Sparrow(5, 'blue', 'meat', 7)
anim.eat()
print(anim.can_fly)