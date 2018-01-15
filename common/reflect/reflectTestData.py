def method1(a, b):
    print("do method1")
    print(a, b)
    return a + b


def method2():
    print("do method2")
    return "method2"


class MethodDemo(object):
    def class_method1(self, a, b):
        print("do class method1")
        print(a, b)
        return a + b

    def class_method2(self):
        print("do class_method2")
        return "class_method2"


if __name__ == "__main__":
    m = MethodDemo()
    print(hasattr(m, "class_method1"))
    func = getattr(m, "class_method1")
    func(1, 2)
