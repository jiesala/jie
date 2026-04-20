def cclt(x):
    return -3*x**2 + 21.6*x + 1

def fibonacci_search_max(f, a, b, eps):
    """
    斐波那契法求单峰函数最大值
    """
    # 生成斐波那契数列
    F = [1, 1]
    while F[-1] < (b - a) / eps:
        F.append(F[-1] + F[-2])

    n = len(F) - 1

    # 初始两点
    x1 = a + F[n-2] / F[n] * (b - a)
    x2 = a + F[n-1] / F[n] * (b - a)
    f1, f2 = f(x1), f(x2)

    # 迭代收缩
    for k in range(n-1, 1, -1):
        if f1 < f2:      # 最大值在右侧
            a = x1
            x1, f1 = x2, f2
            x2 = a + F[k-2] / F[k] * (b - a)
            f2 = f(x2)
        else:            # 最大值在左侧
            b = x2
            x2, f2 = x1, f1
            x1 = a + F[k-2] / F[k] * (b - a)
            f1 = f(x1)

    return (a + b) / 2


# 测试
best_x = fibonacci_search_max(cclt, 0, 25, 0.001)
print("最优解 x =", best_x)
print("最优值 f(x) =", cclt(best_x))

            a2=cclt(ri)
        else :
            ri,le,len1 = le,le-((len1-(ri-le))/2-(ri-le)),len1-(len1-(ri-le))/2
            a2=a1
            a1=cclt(le)
        nums-=1
    print(le,ri)
    print(cclt(le),cclt(ri))
search(0,25,0.001)
            a2=cclt(ri)
        else :
            ri,le,len1 = le,le-((len1-(ri-le))/2-(ri-le)),len1-(len1-(ri-le))/2
            a2=a1
            a1=cclt(le)
        nums-=1
    print(le,ri)
    print(cclt(le),cclt(ri))
search(0,25,0.001)