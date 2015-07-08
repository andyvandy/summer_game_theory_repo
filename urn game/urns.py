import numpy as np
import itertools


def main():
    max_balls=20
    results = np.zeroes(n,n)
    for i,j in  itertools.product(*[range(max_balls)]):
        states=[(i,j,1)]
        saturated =1
        while staturated:
            
            balls = states[0][0] + states[0][1] -1
            new_states=[(k,balls-k, 0 ) for k in range(balls)]]
            for state in states:
                a,b,c=state
                if a,b >1:
                    new_states[a-2] =(a-2,b+1,new_states[a-2][2]+c*(a*(a-1)/((a+b)*((a-1)+b))))
                    new_states[a] =(a,b-1,new_states[a][2]+c*(b*(b-1)/((a+b)*((b-1)+a))+(b*a/((a+b)*((b-1)+a)))+(b*a/((a+b)*((a-1)+b)))))
                elif a >1:
                    new_states[a-2] =(a-2,b+1,new_states[a-2][2]+c*(a*(a-1)/((a+b)*((a-1)+b))))
                    new_states[a] =(a,b-1,new_states[a][2]+c*((b*a/((a+b)*((b-1)+a)))+(b*a/((a+b)*((a-1)+b)))))
                elif b>1:    
                    new_states[a] =(a,b-1,new_states[a][2]+c*((b*(b-1)/((a+b)*((b-1)+a)))+((b*a/((a+b)*((b-1)+a)))+(b*a/((a+b)*((a-1)+b)))))

                elif a==1 and b==1:
                    new_states[a] =(1,0,new_states[a][2]+c)
                else:
                    new_states[a]=(1,0,new_states[a][2]+c)
            if new_states=states:
                saturated=0
            states = new_states
                
                
if __name__ =="__main__":
    main()