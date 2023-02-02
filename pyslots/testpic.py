
import matplotlib.pyplot as plt
if __name__ == '__main__':
    x = range(10)
    y = [3,1,2,9,6,2,1,8,10,8]
    l = plt.plot(x, y)
    plt.xlabel("x")
    plt.xlabel("y")
    plt.legend()
    plt.show()
    print("hello")