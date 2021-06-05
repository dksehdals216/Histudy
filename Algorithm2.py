#Set constraints
Min_number_of_member = 4
Max_number_of_member = 6
#Scoring policy
First_preference = 10
Second_preference = 7
Third_preference = 5

import pandas as pd

data = pd.read_excel('data2.xlsx')[:33].fillna('-1')

print(type(data))

import numpy as np

data.columns = ['Timestamp','Email','Group','PrevGroup','studentNum','Name','Gender','PhoneNumber','StudyTypes','GroupMember'
             ,'FirstCode','FirstClassName','FirstClassProf','SecondCode','SecondClassName','SecondClassProf'
             ,'ThirdCode','ThirdClassName','ThirdClassProf','Extra','English',"with_club","Isclub","clubName","Agree"]
data_ = data[['Timestamp','GroupMember'
             ,'FirstCode','FirstClassProf','SecondCode','SecondClassProf'
             ,'ThirdCode','ThirdClassProf']]

if np.nan == data_['SecondCode'][10] :
    print("hello")

arr = data_["FirstCode"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr)
d1 = dict((i.upper(),j) for j,i in enum)
arr = data_["SecondCode"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr,start=100)
d3 = dict((i.upper(),j) for j,i in enum)

arr = data_["ThirdCode"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr,start=200)
d5 = dict((i.upper(),j) for j,i in enum)

'''
arr = data_["FirstClassProf"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr)
d2 = dict((i,j) for j,i in enum)
arr = data_["SecondClassProf"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr,start=100)
d4 = dict((i,j) for j,i in enum)
arr = data_["ThirdClassProf"].to_numpy()
unique_arr = np.unique(arr)
enum = enumerate(unique_arr,start=200)
d6 = dict((i,j) for j,i in enum)
'''

d1.update(d3)
d1.update(d5)
d_ = {}
for i, (k, v) in enumerate(d1.items()):
    d_[k] = i
print(d_)

d1 = d_
'''
d2.update(d4)
d2.update(d6)
'''

#print(d1,d2,d3,d4,d5,d6)

l1 = list(np.array(data_['Timestamp'].tolist()))
l2 = list(np.array(data_['FirstCode'].tolist()))
l3 = list(np.array(data_['FirstClassProf'].tolist()))
l4 = list(np.array(data_['SecondCode'].tolist()))
l5 = list(np.array(data_['SecondClassProf'].tolist()))
l6 = list(np.array(data_['ThirdCode'].tolist()))
l7 = list(np.array(data_['ThirdClassProf'].tolist()))
l8 = list(np.array(data_['GroupMember'].tolist()))

l = [[d1[m2.upper()],m3,d1[m4.upper()],m5,d1[m6.upper()],m7,m8.split(',')] for m2,m3,m4,m5,m6,m7,m8 in zip(l2,l3,l4,l5,l6,l7,l8)]

for i in l :
    i[6] = [int(k) for k in i[6]]

for i in l :
    print(i)
    
    
print("ASDF")


dicts = [{} for i in range(len(d1.values()))]

for i in d1.values() :
    num = 0
    for j in l :
        if j[0] == i :
            if j[1] not in dicts[i] :
                dicts[i][j[1]] = num
                num += 1
    for j in l :
        if j[2] == i :
            if j[3] not in dicts[i] :
                dicts[i][j[3]] = num
                num += 1
    for j in l :
        if j[4] == i :
            if j[5] not in dicts[i] :
                dicts[i][j[5]] = num
                num += 1
    
l = [[m1,dicts[m1][m2],m3,dicts[m3][m4],m5,dicts[m5][m6],m7] for (m1,m2,m3,m4,m5,m6,m7) in l]

print("!@#$!@#$!@#$")
for i in l :
    print(i)
    
GenerateGroup = []
GenerateList = []

GetGroupPossible = [i[6] for i in l]
unique_arr = np.unique(GetGroupPossible)
print(unique_arr)

for ind, PosList in enumerate(unique_arr) :
    count = 0
    for id_, i in enumerate(l) :
        if i[6] == PosList :
            i
            if count == 0 :
                count += 1
                get = i # possible?
            else :
                count += 1
    get.append(get[6])
    get[6] = count
    GenerateList.append(get)

for i in GenerateList :
    print(i)
    
print(d1)


lst = GenerateList
class_type = d1.values()
print(class_type)


print("aSDF")
print(dicts)

#Step 2 : Count the first preference
count = [0] * len(class_type)
for element in lst :
    count[element[0]] =  count[element[0]] + element[6]
    
print(count)
total = 0
for i in count :
    total = total + i
print(total)

Min = [ int(num / Min_number_of_member) for num in count]
Max = [ int(num / Max_number_of_member) for num in count]
print(Min)
print(Max)

'''Group_Num_List = []

for i in range(len(class_type)) :
    if not Group_Num_List :
        for j in range(Min[i]-Max[i]+1) :
            Group_Num_List.append([Max[i]+j])
    else :
        lst_tmp = []
        for element in Group_Num_List :
            for j in range(Min[i]-Max[i]+1) :
                tmp = element[:]
                tmp.append(Max[i]+j)
                lst_tmp.append(tmp)
        Group_Num_List = lst_tmp
    
print(len(Group_Num_List))

## How can we reduce the size of assumption?
## Max( Max() , Professor_Num ) ?

print(Group_Num_List[0])'''

Group_Num_List = [Min]

#Step3 Group with the first preference for each assumption

#Get list of student index of each first preference
List_of_first_preference_for_each_Class_Type = []
for i in range(len(class_type)) :
    ## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tmp = [[] for i in range(3)]
    for idx, j in enumerate(lst) :
        # idx refers to student index
        # j[0] is the first preference subject
        if j[0] == i :
            tmp[j[1]].append(idx)
    List_of_first_preference_for_each_Class_Type.append(tmp)

for classes in List_of_first_preference_for_each_Class_Type :
    for professor in classes :
        professor.sort(key=lambda x : lst[x][6], reverse=True)

print(List_of_first_preference_for_each_Class_Type)

List_of_second_preference_for_each_Class_Type = []
for i in range(len(class_type)) :
    ## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tmp = [[] for i in range(3)]
    for idx, j in enumerate(lst) :
        # idx refers to student index
        # j[0] is the first preference subject
        if j[2] == i :
            tmp[j[3]].append(idx)
    List_of_second_preference_for_each_Class_Type.append(tmp)
    

print(List_of_second_preference_for_each_Class_Type)

for classes in List_of_second_preference_for_each_Class_Type :
    for professor in classes :
        professor.sort(key=lambda x : lst[x][6], reverse=True)
    

List_of_third_preference_for_each_Class_Type = []
for i in range(len(class_type)) :
    ## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tmp = [[] for i in range(3)]
    for idx, j in enumerate(lst) :
        # idx refers to student index
        # j[0] is the first preference subject
        if j[4] == i :
            tmp[j[5]].append(idx)
    List_of_third_preference_for_each_Class_Type.append(tmp)
    
for classes in List_of_third_preference_for_each_Class_Type :
    for professor in classes :
        professor.sort(key=lambda x : lst[x][6], reverse=True)
        
print(List_of_third_preference_for_each_Class_Type)

def checkIfThereIsMinimum(array) :
    for id_, i in enumerate(array) :
        if Max_number_of_member - i <= Min_number_of_member :
            return id_
    return -1

def Remove(array, i) :
    for l, class_ in enumerate(array) :
        for m, class_num in enumerate(class_) :
            for n, stu in enumerate(class_num) :
                if stu == i :
                    array[l][m].remove(i)
                    return True;
    print(i)
    print("error")
    return False;

def RemoveAll(array, i) :
    count = []
    for l, class_ in enumerate(array) :
        for m, class_num in enumerate(class_) :
            for n, stu in enumerate(class_num) :
                if stu == i :
                    count.append(l)
                    array[l][m].remove(i)
    if len(count) >= 1 :
        return count
    return False

from copy import deepcopy
assumption_score = [0] * len(Group_Num_List)
#find the best way for each assumption
#after finding the best assumption than distribute!
for a_i, assumption in enumerate(Group_Num_List) :
    #여기서 Group_Num_List는 가능한 assumption 즉 각 과목마다 Maximum Class 수를 정의 해둔 것이다.
    #이는 알고리듬의 경의 수를 Maximum Class를 정의 함으할려고 한 것이지만
    #그럼에도 M^N의 (M은 MinGroupNum - MaxGroupNum, N은 class 개수) 복잡도를 가지고 있어 현실적으로 구현 불가능할 것으로 보인다
    #또한 First preference의 Maximum profit이 Second preference와 Third preference 요소들을 추가하는 방법에 따라 더 다양한 경우의 수가 발생하며
    #(M^N*O^P*Q^R) 다만, (P,R)은 M보다는 상대적으로 작은 수 일것이다.
    #마지막으로 First preference의 Maximum profit의 경우가 greedy가 아니다. (물론 대부분의 경우에 대해서 greedy일 것으로 생각되었기 때문에 알고리듬을 이렇게 구성하였다)
    #따라서 Assumption을 사용하는 것은 일단 미지의 영역으로 남겨두고
    #최대한 많은 그룹을 만들수 있도록 하는게 대부분의 경우에 대해서 최대의 효율을 보일 수 있다고 생각하여
    #현 코드에서 assumption을 Min = [ int(num / Min_number_of_member) for num in count]로 두었다.
    
    #find the best way for each class between student in the same first preference
    #copy list
    First = deepcopy(List_of_first_preference_for_each_Class_Type)
    Second = deepcopy(List_of_second_preference_for_each_Class_Type)
    Third = deepcopy(List_of_third_preference_for_each_Class_Type)
    Output_Bottle = []
    Bottle_record = []
    Bottle_index_record = []
    STU_COUNT = []
    
    # 첫번째 선호도를 가지고 그룹 편성하는 방법은 총 3단계로 구성 되어있다.
    #1. 일단은 같은 교수님이 있는 학생들끼리만 배정하면서 가능한 넓게 학생들을 분포시킨다.
    #2. 동일한 교수님임에도 가능하게 넓게 분포시킴으로써 마지막에 인원이 적어 그룹에 못 들어간 학생이 있을 수 있다.
    #   그러한 학생들을 다시 한번 남은 자리에 넣을 수 있는지 시도해본다
    #3. 동일한 교수님이 아니라도 넣을 수 있으면 넣는다.
    #4. 첫번째 선호드를 가지고 그룹을 편성했을 때 그룹에 들어가지 못하는 학생이 있을 수 있으며
    #   각 과목마다 남은 학생의 총합이 그룹사이즈의 Min 보다 작아야 한다.
    #이렇게 순차적으로 매칭을 통한 방식은 List의 맨앞에 있는 학생에게 유리하기 때문에
    #공평성을 위해 시작하기전에 List를 Sorting하는 과정이 필요하다.
    
    for idx, group_num_per_class in enumerate(assumption):
    # i refers to each class_Type
        ## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        class_info = List_of_first_preference_for_each_Class_Type[idx]
        
        student_count_with_each_different_professor = [0] * len(First[idx])
        Bottle_index = [-1] * len(First[idx])
        for idx_, students in enumerate(List_of_first_preference_for_each_Class_Type[idx]) :
            for student in students :
                student_count_with_each_different_professor[idx_] += lst[student][6]
        Bottle = [Max_number_of_member for i in range(group_num_per_class)]
        Input_In_the_Bottle = [[] for i in range(group_num_per_class)]
        if group_num_per_class == 0:
            break
            
        for phase in range(len(First[idx])):
            
            if phase == 0 :
                Bottle_index[phase] = 0
                start = 0
                for group_in_first_phase in List_of_first_preference_for_each_Class_Type[idx][phase] :
                    if start == 0 :
                        if student_count_with_each_different_professor[phase] < Min_number_of_member :
                            break
                        else :
                            start = 1
                    if Bottle[Bottle_index[phase]] >= lst[group_in_first_phase][6] :
                        # 현재 병에 자리가 남음
                        if Max_number_of_member - Bottle[Bottle_index[phase]] >= Min_number_of_member :
                            # 충분히 채워져있으면 다음으로
                            if Bottle_index[phase] + 1 >= len(Bottle) :
                                break
                            if student_count_with_each_different_professor[phase] < Min_number_of_member :
                                break
                            Bottle_index[phase] += 1
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)
                            
                        else :
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)
                            
                            
                    else :
                        # 현재 병에 자리가 없어서 다음 병으로 이동
                        
                        # 다음 병으로 이동할 만큼 여유가 있을 때
                        if  student_count_with_each_different_professor[phase] >= Min_number_of_member :
                            if Bottle_index[phase] + 1 >= len(Bottle) :
                                break
                            Bottle_index[phase] += 1
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)

                        
                        # 나중에 index에서 부터 출발해서 다음 병으로 이동할 만큼 여유가 없을 때 일단 킵해둠
            else :
                start = 0
                if Bottle_index[phase-1]+1 >= len(Bottle) :
                    break
                if Bottle_index[phase-1] == 0 and Bottle[0] == 6 :
                    Bottle_index[phase] = Bottle_index[phase-1]
                else :
                    Bottle_index[phase] = Bottle_index[phase-1]+1
                for group_in_first_phase in List_of_first_preference_for_each_Class_Type[idx][phase] :
                    if start == 0 :
                        if student_count_with_each_different_professor[phase] < Min_number_of_member :
                            break
                        else :
                            start = 1
                    if Bottle[Bottle_index[phase]] >= lst[group_in_first_phase][6] :
                        # 현재 병에 자리가 남음
                        if Max_number_of_member - Bottle[Bottle_index[phase]] >= Min_number_of_member :
                            # 충분히 채워져있으면 다음으로
                            if Bottle_index[phase] + 1 >= len(Bottle) :
                                break
                            if student_count_with_each_different_professor[phase] < Min_number_of_member :
                                break
                            Bottle_index[phase] += 1
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)

                        else :
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)

                    else :
                        # 현재 병에 자리가 없어서 다음 병으로 이동
                        
                        # 다음 병으로 이동할 만큼 여유가 있을 때
                        if student_count_with_each_different_professor[phase] >= Min_number_of_member :
                            #index 초과
                            if Bottle_index[phase] + 1 >= len(Bottle) :
                                break
                            Bottle_index[phase] += 1
                            Bottle[Bottle_index[phase]] -= lst[group_in_first_phase][6]
                            Input_In_the_Bottle[Bottle_index[phase]].append((group_in_first_phase,lst[group_in_first_phase][1],lst[group_in_first_phase][6]))
                            student_count_with_each_different_professor[phase] -= lst[group_in_first_phase][6]
                            First[idx][phase].remove(group_in_first_phase)
                            Remove(Second,group_in_first_phase)
                            Remove(Third,group_in_first_phase)
                        
                        # 나중에 index에서 부터 출발해서 다음 병으로 이동할 만큼 여유가 없을 때 일단 킵해둠
        Output_Bottle.append(Input_In_the_Bottle)
        Bottle_record.append(Bottle)
        Bottle_index_record.append(Bottle_index)
        STU_COUNT.append(student_count_with_each_different_professor)
        
        #print(Input_In_the_Bottle)
        #print(Input_In_the_Bottle)
        # 나중에 중간에 Min Max가 5, 8 이면 문제가 생길 수 있으면, phase 다음 과정에 Min 한게 들어갔는지 검증하는 것을 포함시켜야함
    for idx, group_num_per_class in enumerate(assumption):
        for idx_ , group_in_first_phase in enumerate(First[idx]) :
            #idx is a class
            #idx_ is a phase
            if idx_ == len(First[idx])-1 :
                for i in group_in_first_phase :
                    # i is one group
                    for j in range(Bottle_index_record[idx][idx_],len(Bottle_record[idx])) :
                        if Bottle_record[idx][j] >= lst[i][6] :
                            Bottle_record[idx][j] -= lst[i][6]
                            Output_Bottle[idx][j].append((i,lst[i][1],lst[i][6]))
                            STU_COUNT[idx][idx_] -= lst[i][6]
                            First[idx][idx_].remove(i)
                            Remove(Second,i)
                            Remove(Third,i)
                            break
                           
            else :
                for i in group_in_first_phase :
                    for j in range(Bottle_index_record[idx][idx_],Bottle_index_record[idx][idx_+1]) :
                        if Bottle_record[idx][j] >= lst[i][6] :
                            Bottle_record[idx][j] -= lst[i][6]
                            Output_Bottle[idx][j].append((i,lst[i][1],lst[i][6]))
                            STU_COUNT[idx][idx_] -= lst[i][6]
                            First[idx][idx_].remove(i)
                            Remove(Second,i)
                            Remove(Third,i)
                            break
        #Phase 다 돌았고 혹시 Bottle 중에 Min보다 작게 있으면 비우기가 필요할까?
    #print(First)
    for idx, group_num_per_class in enumerate(assumption):
        for idx_ , group_in_first_phase in enumerate(First[idx]) :
            #idx is a class
            #idx_ is a phase
            for i in group_in_first_phase :
                # i is one group
                
                for j in range(len(Bottle_record[idx])) :
                    if Bottle_record[idx][j] >= lst[i][6] and Bottle_record[idx][j] != Max_number_of_member:
                        Bottle_record[idx][j] -= lst[i][6]
                        Output_Bottle[idx][j].append((i,lst[i][1],lst[i][6]))
                        STU_COUNT[idx][idx_] -= lst[i][6]
                        First[idx][idx_].remove(i)
                        Remove(Second,i)
                        Remove(Third,i)
                        break
    

    #print(Output_Bottle[2])
    #print(Output_Bottle[2])
    '''for k in Output_Bottle :
        for i in k :
            #i phase
            sum = 0
            for j in i :
                sum +=j[2]
            print(sum)'''
    print("Matching Result for first preference")
    for i, K in enumerate(Output_Bottle) :
        Output_Bottle[i] = [ele for ele in K if ele != []]

    print("--End--")
    
    print("First leftovers ")
    print(First)
    print("Count number of First leftovers ")
    print(STU_COUNT)
    print("Second leftovers ")
    print(Second)
    print("third leftovers ")
    print(Third)
                
    print("Matching Result for first preference")
    for i, K in enumerate(Output_Bottle) :
        print("-------------"+str(i)+"-----------")
        print(K)


# 두번째 선호도를 가지고 그룹 편성하는 방법은 총 3단계로 구성 되어있다.

#1단계 : 첫번째, 두번째 선호도를 가지고 Minimum Group을 만들 수 있는 방법이 있는지 탐색한다
#2단계 : 이때 Rare한 그룹이 우선 배정 될 수 있도록 가장 학생의 수가 적은 그룹이 먼저 배정 될 수 있도록 Sorting을 한다.
#3단계 : 최대한 그룹이 많을 수 있도록 분배한다.
#4단계 : 다시 한번 채워보고,
#5단계 : 기존 그룹안에 배정할 공간이 남아있을 경우 그곳으로 분배한다.
#5단계를 1단계 보다 앞에 두지 않는 이유는 동일한 교수님의 분반으로 배정하는 것 보다 최대한 많은 학생이 첫번째, 두번째 preference 안에서 배정 받을 수 있도록 하기
#위함이다.
#이렇게 순차적으로 매칭을 통한 방식은 List의 맨앞에 있는 학생에게 유리하기 때문에
#공평성을 위해 시작하기전에 List를 Sorting하는 과정이 필요하다.
    
    ## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class_info = Second

STU_COUNT2 = []

#1단계 : 첫번째, 두번째 선호도를 가지고 Minimum Group을 만들 수 있는 방법이 있는지 탐색한다

#Second [class, class_type, student]
for idx_, class_ in enumerate(Second) :
    count_ = [0] * len(class_)
    for i_, Class_type in enumerate(class_) :
        for j_, student in enumerate(Class_type) :
            count_[i_] += lst[student][6]
    STU_COUNT2.append(count_)

First_Second = []
for first, second in zip(STU_COUNT,STU_COUNT2) :
    Sum = [x+y for x,y in zip(first, second)]
    First_Second.append(Sum)
    
First_Second_Total = [[i,sum(x)] for i, x in enumerate(First_Second) if sum(x) >= Min_number_of_member]
#2단계 : 이때 Rare한 그룹이 우선 배정 될 수 있도록 가장 학생의 수가 적은 그룹이 먼저 배정 될 수 있도록 Sorting을 한다.
First_Second_Total_sort = sorted(First_Second_Total, key=lambda x: x[1])


FirstAndSecond = deepcopy(First)

#Frist 뒤에 Second를 append 하여 First가 먼저 배정 될 수 있도록 한다.
for first, second in zip(FirstAndSecond,Second) :
    for i in range(len(first)) :
        first[i].extend(second[i])

#3단계 : 동일한 분반이 최대한 많을 수 있도록 분배한다.
Bottle = Max_number_of_member
new_Bottle_List = [ [] for i in range(len(class_type))]
BottleInput = []

while(True) :
    
    if len(First_Second_Total_sort) == 0 :
        break
        
    (class_id,Number) = First_Second_Total_sort[0]
    # 먼저 Bottle 에 넣을 수 있는지 확인
    
    while(Max_number_of_member-Bottle<Min_number_of_member) :
        for P, Class_type in enumerate(FirstAndSecond[class_id]) :
            if Class_type :
                student = Class_type.pop(0) # 맨 앞 원소 가져오기 동시에 삭제
                BottleInput.append((student,lst[student][3],lst[student][6]))
                Bottle -= lst[student][6]
                First_Second_Total_sort[0][1] -= lst[student][6]
                
                arr = RemoveAll(FirstAndSecond,student)
                if arr :
                    for i in arr : #i is class
                        for j in First_Second_Total_sort :
                            if j[0] == i :
                                j[1] -= lst[student][6]
                                break
                        
                Remove(First,student)
                Remove(Second,student)
                Remove(Third,student)
        if First_Second_Total_sort[0][1]+Max_number_of_member-Bottle < Min_number_of_member :
            print("break")
            break
                
    First_Second_Total_sort = [i for i in First_Second_Total_sort if i[1] >= Min_number_of_member]
    # Min 보다 큰 것만 남겨둠
    First_Second_Total_sort.sort(key=lambda x: x[1])
    new_Bottle_List[class_id].append(BottleInput)
    Bottle = Max_number_of_member
    BottleInput = []
    
print(new_Bottle_List)

#4-1단계 bottle 합치기
for class1, class2 in zip(Output_Bottle,new_Bottle_List) :
    class1.extend(class2)
    
print("Matching Result for first preference")
for i, K in enumerate(Output_Bottle) :
    print("-------------"+str(i)+"-----------")
    print(K)

print("Matching Result for first preference")
for i, K in enumerate(new_Bottle_List) :
    print("-------------"+str(i)+"-----------")
    print(K)
    
#4단계 bottle에 넣을 수 있는 만큼 일단 넣어보기
    
for id, class_ in enumerate(Output_Bottle) :
        for bottle in class_ :
            for Class_type in FirstAndSecond[id] :
                #[72], [], [126]
                for student in Class_type :
                    if sum(i[2] for i in bottle) + lst[student][6] <= Max_number_of_member :
                        bottle.append((student,lst[student][3],lst[student][6]))
                        Remove(First,student)
                        Remove(Second,student)
                        Remove(Third,student)
                        RemoveAll(FirstAndSecond,student)
                        print("!!!",student)
                        break;

print("Matching Result for first preference")
for i, K in enumerate(Output_Bottle) :
    print("-------------"+str(i)+"-----------")
    print(K)


# 두번째 선호도를 가지고 그룹 편성하는 방법은 총 3단계로 구성 되어있다.

#1단계 : 첫번째, 두번째 선호도를 가지고 Minimum Group을 만들 수 있는 방법이 있는지 탐색한다
#2단계 : 이때 Rare한 그룹이 우선 배정 될 수 있도록 가장 학생의 수가 적은 그룹이 먼저 배정 될 수 있도록 Sorting을 한다.
#3단계 : 최대한 그룹이 많을 수 있도록 분배한다.
#4단계 : 다시 한번 채워보고,
#5단계 : 기존 그룹안에 배정할 공간이 남아있을 경우 그곳으로 분배한다.
#5단계를 1단계 보다 앞에 두지 않는 이유는 동일한 교수님의 분반으로 배정하는 것 보다 최대한 많은 학생이 첫번째, 두번째 preference 안에서 배정 받을 수 있도록 하기
#위함이다.
#이렇게 순차적으로 매칭을 통한 방식은 List의 맨앞에 있는 학생에게 유리하기 때문에
#공평성을 위해 시작하기전에 List를 Sorting하는 과정이 필요하다.

## number 3 should be changed after implementation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class_info = Third

STU_COUNT = []

for idx_, class_ in enumerate(First) :
    count_ = [0] * len(class_)
    for i_, Class_type in enumerate(class_) :
        for j_, student in enumerate(Class_type) :
            count_[i_] += lst[student][6]
    STU_COUNT.append(count_)
    
STU_COUNT2 = []

for idx_, class_ in enumerate(Second) :
    count_ = [0] * len(class_)
    for i_, Class_type in enumerate(class_) :
        for j_, student in enumerate(Class_type) :
            count_[i_] += lst[student][6]
    STU_COUNT2.append(count_)
    
STU_COUNT3 = []

#1단계 : 첫번째, 두번째 선호도를 가지고 Minimum Group을 만들 수 있는 방법이 있는지 탐색한다

#Second [class, class_type, student]
for idx_, class_ in enumerate(Third) :
    count_ = [0] * len(class_)
    for i_, Class_type in enumerate(class_) :
        for j_, student in enumerate(Class_type) :
            count_[i_] += lst[student][6]
    STU_COUNT3.append(count_)

First_Third = []
for first, second, third in zip(STU_COUNT,STU_COUNT2,STU_COUNT3) :
    Sum = [x+y+z for x,y,z in zip(first, second, third)]
    First_Third.append(Sum)
    
First_Third_Total = [[i,sum(x)] for i, x in enumerate(First_Third) if sum(x) >= Min_number_of_member]
#2단계 : 이때 Rare한 그룹이 우선 배정 될 수 있도록 가장 학생의 수가 적은 그룹이 먼저 배정 될 수 있도록 Sorting을 한다.
First_Third_Total_sort = sorted(First_Third_Total, key=lambda x: x[1])

FirstAndThird = deepcopy(First)

#Frist 뒤에 Third를 append 하여 First가 먼저 배정 될 수 있도록 한다.
for first, second in zip(FirstAndThird,Second) :
    for i in range(len(first)) :
        first[i].extend(second[i])
        
for first, third in zip(FirstAndThird,Third) :
    for i in range(len(first)) :
        first[i].extend(third[i])

#임의로 생성하여 진행할 것이며 나중에 꼭 지워주세요!
#3단계 : 동일한 분반이 최대한 많을 수 있도록 분배한다.
Bottle = Max_number_of_member
new_Bottle_List = [ [] for i in range(len(class_type))]
BottleInput = []

while(True) :
    
    if len(First_Third_Total_sort) == 0 :
        break
        
    (class_id,Number) = First_Third_Total_sort[0]
    # 먼저 Bottle 에 넣을 수 있는지 확인
    
    while(Max_number_of_member-Bottle<Min_number_of_member) :
        for Class_type in FirstAndThird[class_id] :
            if Class_type :
                student = Class_type.pop(0) # 맨 앞 원소 가져오기 동시에 삭제
                BottleInput.append((student,lst[student][3],lst[student][6]))
                Bottle -= lst[student][6]
                First_Third_Total_sort[0][1] -= lst[student][6]
                
                arr = RemoveAll(FirstAndThird,student)
                if arr :
                    for i in arr : #i is class
                        for j in First_Third_Total_sort :
                            if j[0] == i :
                                j[1] -= lst[student][6]
                                break
                        
                Remove(First,student)
                Remove(Second,student)
                Remove(Third,student)
        if First_Third_Total_sort[0][1]+Max_number_of_member-Bottle < Min_number_of_member :
            print("break")
            break
                
    First_Third_Total_sort = [i for i in First_Third_Total_sort if i[1] >= Min_number_of_member]
    # Min 보다 큰 것만 남겨둠
    First_Third_Total_sort.sort(key=lambda x: x[1])
    new_Bottle_List[class_id].append(BottleInput)
    Bottle = Max_number_of_member
    BottleInput = []
    
print(new_Bottle_List)

#4-1단계 bottle 합치기
for class1, class2 in zip(Output_Bottle,new_Bottle_List) :
    class1.extend(class2)
    
print("Matching Result for first preference")
for i, K in enumerate(Output_Bottle) :
    print("-------------"+str(i)+"-----------")
    print(K)

print("Matching Result for first preference")
for i, K in enumerate(new_Bottle_List) :
    print("-------------"+str(i)+"-----------")
    print(K)
    
#4단계 bottle에 넣을 수 있는 만큼 일단 넣어보기
    
for id, class_ in enumerate(Output_Bottle) :
        for bottle in class_ :
            for Class_type in FirstAndThird[id] :
                #[72], [], [126]
                for student in Class_type :
                    if sum(i[2] for i in bottle) + lst[student][6] <= Max_number_of_member :
                        bottle.append((student,lst[student][3],lst[student][6]))
                        Remove(First,student)
                        Remove(Second,student)
                        Remove(Third,student)
                        RemoveAll(FirstAndThird,student)
                        print("!!!",student)
                        break;

print("Matching Result for first preference")
for i, K in enumerate(Output_Bottle) :
    print("-------------"+str(i)+"-----------")
    print(K)

lst = ['그룹', '학번']
  
# Calling DataFrame constructor on list
dframe = pd.DataFrame(columns=lst)
print(dframe)

count = 0
group_id = 0

for i, K in enumerate(Output_Bottle) :
    for group in K :
        for s_groups in group :
        #s_group is a index of GenerateList
            group_id += 1
            for stu in GenerateList[s_groups[0]][7] :
                count += 1
                dframe.loc[count] = [group_id,stu]

print(dframe)
print(GenerateList)
dframe.to_csv('result2.csv',index=False)




#for i in range(5) :
#    dframe.loc[i] = ['name' + str(i)] + list(randint(10, size=2))

