from abc import ABCMeta, abstractmethod


class IProduct(metaclass=ABCMeta):
    pass


class ICreator(metaclass=ABCMeta):
    @abstractmethod
    def create_product(self) -> IProduct:
        """Method to create a product instance."""
        pass


class Logic:
    def __init__(self, creator: ICreator):
        self.creator = creator

    def run(self) -> IProduct:
        """Run the logic to create a product."""
        product = self.creator.create_product()
        return product


class ConcreteProduct(IProduct):
    def __init__(self):
        self.name = "Concrete Product"


class ConcreteCreator(ICreator):
    def create_product(self) -> IProduct:
        return ConcreteProduct()


if __name__ == "__main__":
    creator = ConcreteCreator()
    logic = Logic(creator)
    product = logic.run()
    print(product.name)  # Output: Concrete Product
