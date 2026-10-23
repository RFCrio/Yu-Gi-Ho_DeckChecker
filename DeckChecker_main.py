from DeckChecker_controller import DeckController
from DeckChecker_model import DeckRepository, YgoprodeckAPI
from DeckChecker_view import ConsoleView


def main() -> None:
    DeckController(
        repo=DeckRepository('Checker.json'),
        api=YgoprodeckAPI(),
        view=ConsoleView(),
    ).run()


if __name__ == '__main__':
    main()
