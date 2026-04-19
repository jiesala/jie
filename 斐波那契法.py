def cclt(x):
    return -3*x**2+21.6*x+1
def search(left,right,accuracy) :
    len1=right-left
    Fe=[1,1]
    while True :
        if len1/Fe[-1] <= accuracy :
            break
        Fe.append(Fe[-1]+Fe[-2])
    ri=left+Fe[-2]/Fe[-1]*len1
    le=right-Fe[-2]/Fe[-1]*len1
    a1 = cclt(le)
    a2 = cclt(ri)
    nums=len(Fe)-1
    while nums > 0 :
        if a1 <= a2 :
            le,ri,len1 = ri,ri+((len1-(ri-le))/2-(ri-le)),len1-(len1-(ri-le))/2
            a1=a2
            a2=cclt(ri)
        else :
            ri,le,len1 = le,le-((len1-(ri-le))/2-(ri-le)),len1-(len1-(ri-le))/2
            a2=a1
            a1=cclt(le)
        nums-=1
    print(le,ri)
    print(cclt(le),cclt(ri))
search(0,25,0.001)