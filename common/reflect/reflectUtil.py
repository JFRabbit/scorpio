class Reflect(object):
    """
    Python 反射
    """

    def __init__(self, module_name, from_name, method_name, args=(), class_name=""):
        """
        :param module_name:     模块名称 例: A.B
        :param from_name:       from name 例: from A.B
        :param method_name:     方法名
        :param args:            方法入参 例: (1, 2)
        :param class_name:      类名
        :return:                反射方法返回值
        """
        self.module_name = module_name
        self.method_name = method_name
        self.from_name = from_name
        self.args = args
        self.class_name = class_name

    def run(self):
        """ run reflect"""
        mod = __import__(self.module_name, fromlist=list(self.from_name))

        if self.class_name != "":
            if hasattr(mod, self.class_name):
                clazz = getattr(mod, self.class_name)
                if hasattr(clazz, self.method_name):
                    func = getattr(clazz, self.method_name)
                    if len(self.args) == 0:
                        return func(clazz)

                    return func(clazz, *self.args)
                else:
                    raise Exception("Class %s have no method %s" % (self.class_name, self.method_name))
            else:
                raise Exception("Module %s have no Class %s" % (self.module_name, self.class_name))
        else:
            if hasattr(mod, self.method_name):
                func = getattr(mod, self.method_name)
                if len(self.args) == 0:
                    return func()

                return func(*self.args)
            else:
                raise Exception("Module %s have no method %s" % (self.module_name, self.method_name))


if __name__ == '__main__':
    print(help(Reflect))
    import time

    time.sleep(1)

    test_module_name = "common.reflect.reflectTestData"
    test_from_name = "from common.reflect.reflectTestData import MethodDemo"
    test_args = (1, 2)
    test_class_name = "MethodDemo"

    reflect = Reflect(test_module_name, test_from_name, "method1", test_args)
    print(reflect.run())
    print("=" * 30)

    reflect = Reflect(test_module_name, test_from_name, "class_method1", test_args, test_class_name)
    print(reflect.run())
    print("=" * 30)

    reflect = Reflect(test_module_name, test_from_name, "method2")
    print(reflect.run())
    print("=" * 30)

    reflect = Reflect(test_module_name, test_from_name, "class_method2", class_name=test_class_name)
    print(reflect.run())
    print("=" * 30)
