import json
import xml.etree.ElementTree
from abc import ABC, abstractmethod


class DisplayInterface(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


class PrintBookInterface(ABC):
    @abstractmethod
    def print_book(self, title: str, content: str) -> None:
        pass


class SerializeInterface(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


class ConsoleDisplay(DisplayInterface):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplay(DisplayInterface):
    def display(self, content: str) -> None:
        print(content[::-1])


class ConsolePrinter(PrintBookInterface):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrinter(PrintBookInterface):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class JsonSerializer(SerializeInterface):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class XmlSerializer(SerializeInterface):
    def serialize(self, title: str, content: str) -> str:
        root = xml.etree.ElementTree.Element("book")
        xml.etree.ElementTree.SubElement(root, "title").text = title
        xml.etree.ElementTree.SubElement(root, "content").text = content
        return xml.etree.ElementTree.tostring(root, encoding="unicode")


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def display(self, display_interface: DisplayInterface) -> None:
        display_interface.display(self.content)

    def print_book(self, print_interface: PrintBookInterface) -> None:
        print_interface.print_book(self.title, self.content)

    def serialize(self, serialize_interface: SerializeInterface) -> str:
        return serialize_interface.serialize(self.title, self.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "reverse":
                book.display(ReverseDisplay())
            else:
                book.display(ConsoleDisplay())
        elif cmd == "print":
            if method_type == "reverse":
                book.print_book(ReversePrinter())
            else:
                book.print_book(ConsolePrinter())
        elif cmd == "serialize":
            if method_type == "json":
                return book.serialize(JsonSerializer())
            elif method_type == "xml":
                return book.serialize(XmlSerializer())


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
