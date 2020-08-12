from abc import ABC, abstractmethod, abstractproperty


class BasicView(ABC):
    @abstractmethod
    def show(self):
        pass


class BasicController(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def new(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def complete(self):
        pass

    @abstractmethod
    def go_to_line(self):
        pass

    @abstractmethod
    def random(self):
        pass

    @abstractmethod
    def read_complete(self):
        pass

    @abstractmethod
    def show_completed(self):
        pass


class BasicModel(ABC):
    @abstractmethod
    def new(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractproperty
    def count(self):
        pass

    @abstractmethod
    def complete(self):
        pass
