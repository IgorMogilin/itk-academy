from datetime import datetime


class DateMeta(type):
    """Метакласс для добавления временных меток."""

    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class Example(metaclass=DateMeta):
    pass


test_value = Example()

print(test_value.created_at)
