student_score = input("enter list").split()
for n in range(0, len(student_score)):
    student_score[n] = int(student_score[n])
    
print(student_score)

count = 0 

for score in student_score:
    if score > count:
        count = score
        


print("print", count)    
