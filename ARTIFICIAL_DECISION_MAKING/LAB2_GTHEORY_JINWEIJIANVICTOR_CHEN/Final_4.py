import random
if __name__ == '__main__':
 print("RobotA and RobotB working")

 #initialize the count of how the tasks are allocated at the end
countA_1 = 0
countA_2 = 0
countA_3 = 0

countB_1 = 0
countB_2 = 0
countB_3 = 0

cumulative_payoff_A = 0
cumulative_payoff_B = 0
# Define the outcomes and their corresponding probabilities

for i in range(100):
    outcomes_RB = [1, 2, 3] # 1:sorting, 2: delivering, 3: inspecting
    probabilities_B = [0.1,0.1,0.8] #robotB only wants to sort pachages around 10 percent of the time

    # Use random.choices() to randomly select based on probabilities
    result_B = random.choices(outcomes_RB, probabilities_B)
    print(f"Bchoose {result_B}")

    # random.choices() returns a list, so we access the first item

    if result_B[0] == 1 :  # only if B want to go do some sorting since b doing delivering is pretty bad
        
        print("Robot B sorting packages")
        cumulative_payoff_B -= 8
        countB_1 +=1
        if countA_2 != 0 and countA_3 != 0: # if Robot A has done both other tasks just select one randomly 
            outcomes_RA = [2,3]
            probabilities_A = [0.7,0.3]
            result_A= random.choices(outcomes_RA, probabilities_A)
            
            if result_A[0] == 2:
                print("Robot A delivering package")
                print("One rotation finished!!!\n")
                countA_2 +=1
                cumulative_payoff_A -= 6
                i+=1
            else:
                ("Robot A inspecting equipment")
                print("One rotation finished!!!\n")
                countA_3 +=1
                cumulative_payoff_A -= 17
                i+=1

        if countA_2 == 0: #count how many times A has delivered package
            print("Robot A delivering package") #delivers package
            print("One rotation finished!!!\n")
            cumulative_payoff_A -= 6
            countA_2 +=1
            i+=1
        elif countA_3 == 0: 
            print("robot A inspecting equipment")
            print("One rotation finished!!!\n")
            cumulative_payoff_A -= 17
            countA_3 +=1
            i+=1
        
        
    elif result_B[0] == 2 :
        print("Robot B delivering package")
        print("Robot A sorting packages")
        print("One rotation finished!!!\n")
        countA_1 +=1
        countB_2 +=1
        cumulative_payoff_B -= 13
        i+=1
    else:  # = 3
        print("Robot B inspecting equipment")
        print("Robot A sorting packages")
        print("One rotation finished!!!\n")
        countA_1 +=1
        countB_3 +=1
        cumulative_payoff_B -= 3
        i+=1
print(f"Robot A did:[sorting packages: {countA_1} times.\nDelivering packages: {countA_2} times.\nInspecting equipment {countA_3} times\n")
print(f"Robot B did:[sorting packages: {countB_1} times.\nDelivering packages: {countB_2} times.\nInspecting equipment {countB_3} times\n")
print(f"Cumulative payoff Robot A = {cumulative_payoff_A}\nCumulative payoff Robot B = {cumulative_payoff_B}")
