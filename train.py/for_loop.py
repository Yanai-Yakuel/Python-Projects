student_hight = input("enter list").split()
for n in range(0, len(student_hight)):
    student_hight[n] = int(student_hight[n])
print(student_hight)

number_sum = 0 
len = 0

for i in student_hight:
    number_sum += i

for b in student_hight:
    len += 1

#a = len(student_hight)

f = round(number_sum / len)



print(f"the avrage of numbers is ",f)

    