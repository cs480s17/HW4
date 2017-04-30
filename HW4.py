


def main():
    I = float(0)
    II = float(0)
    III = float(0)
    IV = float(0)
    f = open('testdata', 'r')

    while(f.readline()):
        for i in range(28):
            print(f.readline())


if __name__ == "__main__":
    main()