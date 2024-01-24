from abc import ABC, abstractmethod


class Parent(ABC):

    def method_parent(self):
        data = self._parent_method()
        return data * 5

    @abstractmethod
    def _parent_method(self):
        pass


class A(Parent):
    def _parent_method(self):
        data = 10
        print("A's work")
        return data


class B(Parent):
    def _parent_method(self):
        data = 20
        print("B's work")
        return data


class C(Parent):
    def _parent_method(self):
        data = 30
        print("C's work")
        return data


# Example usage
a = A()
print(a.method_parent())

b = B()
print(b.method_parent())

c = C()
print(c.method_parent())
