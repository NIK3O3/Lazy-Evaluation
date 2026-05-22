from __future__ import annotations

import argparse
from itertools import islice
from typing import Any, Callable, Iterable, Iterator, TypeVar


T = TypeVar("T")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Допоміжні функції
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Повертає перші n елементів lazy, без створення списку."""
    return islice(iterable, n)


def debug(x: T) -> T:
    print(f"Processing {x}")
    return x


# ---------------------------------------------------------------------------
# Базові lazy-функції
# ---------------------------------------------------------------------------

def generate_numbers(n: int) -> Iterator[int]:
    """Повертає числа від 1 до n через yield."""
    for number in range(1, n + 1):
        yield number


def lazy_square(data: Iterable[int]) -> Iterator[int]:
    """Повертає генератор квадратів."""
    for item in data:
        yield item * item


def lazy_filter(func: Callable[[T], bool], data: Iterable[T]) -> Iterator[T]:
    """Працює як filter, але реалізовано через yield."""
    for item in data:
        if func(item):
            yield item


def lazy_map(func: Callable[[T], R], data: Iterable[T]) -> Iterator[R]:
    """Працює як map, але реалізовано через yield."""
    for item in data:
        yield func(item)


def pipeline(data: Iterable[Any], steps: list[Callable[[Iterable[Any]], Iterable[Any]]]) -> Iterable[Any]:
    """Послідовно застосовує steps. Якщо steps lazy, pipeline теж lazy."""
    result: Iterable[Any] = data

    for step in steps:
        result = step(result)

    return result


def run_pipeline(data: Iterable[Any], steps: list[Callable[[Iterable[Any]], Iterable[Any]]]) -> Iterable[Any]:
    """
    Lazy Data Processing Engine:
    - без списків;
    - тільки iterable/generator;
    - обчислення тільки під час ітерації.
    """
    current: Iterable[Any] = data

    for step in steps:
        current = step(current)

    return current


def compose(
    f: Callable[[Iterable[Any]], Iterable[Any]],
    g: Callable[[Iterable[Any]], Iterable[Any]],
) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """
    compose(f, g)(data) == f(g(data)).
    Якщо f і g повертають генератори, композиція також lazy.
    """
    def composed(data: Iterable[Any]) -> Iterable[Any]:
        return f(g(data))

    return composed


def lazy_reduce(
    func: Callable[[R, T], R],
    data: Iterable[T],
    initial: R,
) -> Callable[[], R]:
    """
    Lazy reduce як відкладене terminal-обчислення.

    reduce не може видати фінальний результат без проходу по iterable.
    Але сам запуск reduce можна відкласти: функція повертає compute(),
    і реальна ітерація починається тільки при виклику compute().
    """
    def compute() -> R:
        accumulator = initial

        for item in data:
            accumulator = func(accumulator, item)

        return accumulator

    return compute


# ---------------------------------------------------------------------------
# Завдання 1. Порівняння eager vs lazy
# ---------------------------------------------------------------------------

def task_1_eager_vs_lazy() -> None:
    print_header("Завдання 1. Порівняння eager vs lazy")

    data = [1, 2, 3, 4, 5]

    eager_squares = [x * x for x in data]
    lazy_squares = (x * x for x in data)

    print(f"data = {data}")
    print(f"type(eager_squares) = {type(eager_squares)}")
    print(f"type(lazy_squares) = {type(lazy_squares)}")

    print("\nПрохід по списку квадратів:")
    for value in eager_squares:
        print(value)

    print("\nПрохід по генератору квадратів:")
    for value in lazy_squares:
        print(value)

    print(
        "\nПояснення:\n"
        "- Список квадратів обчислюється одразу. Це eager evaluation.\n"
        "- Генератор квадратів обчислює значення тільки під час ітерації. Це lazy evaluation.\n"
        "- Список тримає всі результати в пам'яті.\n"
        "- Генератор зберігає тільки стан і наступне значення рахує on-demand."
    )


# ---------------------------------------------------------------------------
# Завдання 2. Генератор з yield
# ---------------------------------------------------------------------------

def task_2_generator_with_yield() -> None:
    print_header("Завдання 2. Генератор з yield")

    for x in generate_numbers(5):
        print(x)

    print(
        "\nПояснення:\n"
        "- yield повертає значення і ставить функцію на паузу.\n"
        "- Наступна ітерація продовжує виконання після попереднього yield."
    )


# ---------------------------------------------------------------------------
# Завдання 3. Lazy квадрат
# ---------------------------------------------------------------------------

def task_3_lazy_square() -> None:
    print_header("Завдання 3. Lazy квадрат")

    data = [1, 2, 3, 4, 5]
    result = lazy_square(data)

    print(f"type(result) = {type(result)}")
    print("Квадрати:")
    for value in result:
        print(value)


# ---------------------------------------------------------------------------
# Завдання 4. Lazy filter
# ---------------------------------------------------------------------------

def task_4_lazy_filter() -> None:
    print_header("Завдання 4. Lazy filter")

    data = range(1, 11)
    result = lazy_filter(lambda x: x % 2 == 0, data)

    print(f"type(result) = {type(result)}")
    print("Парні числа:")
    for value in result:
        print(value)


# ---------------------------------------------------------------------------
# Завдання 5. Lazy map
# ---------------------------------------------------------------------------

def task_5_lazy_map() -> None:
    print_header("Завдання 5. Lazy map")

    data = range(1, 6)
    result = lazy_map(lambda x: x * x, data)

    print(f"type(result) = {type(result)}")
    print("Квадрати:")
    for value in result:
        print(value)


# ---------------------------------------------------------------------------
# Завдання 6. Комбінування
# ---------------------------------------------------------------------------

def task_6_combining_lazy_functions() -> None:
    print_header("Завдання 6. Комбінування")

    data = range(1, 10)

    even_numbers = lazy_filter(lambda x: x % 2 == 0, data)
    squares = lazy_map(lambda x: x * x, even_numbers)

    print("lazy_filter(парні) -> lazy_map(квадрати):")
    for value in squares:
        print(value)

    print("\nПроміжні списки не створюються.")


# ---------------------------------------------------------------------------
# Завдання 7. Pipeline
# ---------------------------------------------------------------------------

def task_7_pipeline() -> None:
    print_header("Завдання 7. Pipeline")

    data = range(1, 10)

    result = pipeline(
        data,
        [
            lambda xs: lazy_filter(lambda x: x % 2 == 0, xs),
            lambda xs: lazy_map(lambda x: x * x, xs),
        ],
    )

    print(f"type(result) = {type(result)}")
    print("Результат:")
    for value in result:
        print(value)


# ---------------------------------------------------------------------------
# Завдання 8. Lazy pipeline
# ---------------------------------------------------------------------------

def task_8_lazy_pipeline_first_5() -> None:
    print_header("Завдання 8. Lazy pipeline")

    result = pipeline(
        range(1, 1_000_000),
        [
            lambda xs: lazy_filter(lambda x: x % 2 == 0, xs),
            lambda xs: lazy_map(lambda x: x * x, xs),
        ],
    )

    print("Перші 5 значень:")
    for value in take(5, result):
        print(value)

    print(
        "\nПояснення:\n"
        "- Обчислюються тільки перші 5 результатів.\n"
        "- Весь range(1, 1_000_000) не проходиться повністю.\n"
        "- Жоден проміжний список не створюється."
    )


# ---------------------------------------------------------------------------
# Завдання 9. Відкладене виконання
# ---------------------------------------------------------------------------

def task_9_deferred_execution() -> None:
    print_header("Завдання 9. Відкладене виконання")

    result = pipeline(
        range(1, 6),
        [
            lambda xs: lazy_map(debug, xs),
            lambda xs: lazy_map(lambda x: x * x, xs),
        ],
    )

    print("Pipeline створено. Повідомлення Processing ще не друкувались.")
    print("Починаємо ітерацію:")

    for value in result:
        print(f"Result: {value}")

    print(
        "\nПояснення:\n"
        "- debug(x) викликається тільки тоді, коли for просить наступний елемент.\n"
        "- Саме це і є відкладене виконання."
    )


# ---------------------------------------------------------------------------
# Завдання 10. Обчислення on-demand
# ---------------------------------------------------------------------------

def task_10_on_demand_with_next() -> None:
    print_header("Завдання 10. Обчислення on-demand")

    gen = lazy_map(lambda x: x * x, range(10))

    print(f"type(gen) = {type(gen)}")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")

    print("\nКожен next(gen) обчислює тільки один наступний елемент.")


# ---------------------------------------------------------------------------
# Завдання 11. Великий діапазон
# ---------------------------------------------------------------------------

def task_11_large_range() -> None:
    print_header("Завдання 11. Великий діапазон")

    data = range(10**9)
    result = lazy_map(lambda x: x * 2, data)

    print("Перші 10 елементів після map(x * 2):")
    for value in take(10, result):
        print(value)

    print(
        "\nПояснення:\n"
        "- range(10**9) не створює список з мільярда елементів.\n"
        "- lazy_map не створює список результатів.\n"
        "- Обробляються тільки перші 10 елементів."
    )


# ---------------------------------------------------------------------------
# Завдання 12. Читання файлу, імітація
# ---------------------------------------------------------------------------

def read_lines() -> Iterator[str]:
    """
    Імітація читання файлу через yield.

    У реальному файлі це могло б виглядати так:
        with open('file.txt', encoding='utf-8') as file:
            for line in file:
                yield line.rstrip('\\n')
    """
    lines = [
        "first line",
        "second line",
        "third line",
        "fourth line",
    ]

    for line in lines:
        print(f"Reading: {line}")
        yield line


def task_12_read_lines_simulation() -> None:
    print_header("Завдання 12. Читання файлу, імітація")

    lines = read_lines()

    print("Генератор створено. Рядки ще не прочитані.")
    print("Читаємо перші 2 рядки:")

    for line in take(2, lines):
        print(f"Line: {line}")


# ---------------------------------------------------------------------------
# Завдання 13. Обробка транзакцій, DE-стиль
# ---------------------------------------------------------------------------

def task_13_transactions_de_style() -> None:
    print_header("Завдання 13. Обробка транзакцій, DE стиль")

    transactions = range(1_000_000)

    result = pipeline(
        transactions,
        [
            lambda xs: lazy_filter(lambda x: x % 2 == 0, xs),
            lambda xs: lazy_map(lambda x: x * 10, xs),
        ],
    )

    first_100 = take(100, result)
    total = sum(first_100)

    print("Pipeline: filter(парні) -> map(*10) -> sum перших 100")
    print(f"Результат: {total}")

    print(
        "\nПояснення:\n"
        "- Не обробляється весь range(1_000_000).\n"
        "- Обробляється тільки стільки елементів, скільки потрібно для перших 100 "
        "результатів після filter."
    )


# ---------------------------------------------------------------------------
# Завдання 14. Логування pipeline
# ---------------------------------------------------------------------------

def task_14_pipeline_logging() -> None:
    print_header("Завдання 14. Логування pipeline")

    result = pipeline(
        range(1, 10),
        [
            lambda xs: lazy_map(debug, xs),
            lambda xs: lazy_filter(lambda x: x % 2 == 0, xs),
            lambda xs: lazy_map(lambda x: x * x, xs),
        ],
    )

    print("Беремо тільки перші 3 результати:")
    for value in take(3, result):
        print(f"Output: {value}")

    print("\ndebug показує тільки ті елементи, які реально проходять через pipeline.")


# ---------------------------------------------------------------------------
# Завдання 15. Генерація нескінченної послідовності
# ---------------------------------------------------------------------------

def infinite_numbers() -> Iterator[int]:
    number = 1

    while True:
        yield number
        number += 1


def task_15_infinite_sequence() -> None:
    print_header("Завдання 15. Генерація нескінченної послідовності")

    numbers = infinite_numbers()

    print(f"next(numbers) = {next(numbers)}")
    print(f"next(numbers) = {next(numbers)}")
    print(f"next(numbers) = {next(numbers)}")
    print(f"next(numbers) = {next(numbers)}")
    print(f"next(numbers) = {next(numbers)}")

    print(
        "\nПояснення:\n"
        "- Нескінченний генератор безпечний, якщо брати обмежену кількість значень.\n"
        "- Не можна робити list(infinite_numbers()), бо це нескінченне обчислення."
    )


# ---------------------------------------------------------------------------
# Завдання 16. Compose lazy functions
# ---------------------------------------------------------------------------

def task_16_compose_lazy_functions() -> None:
    print_header("Завдання 16. Compose lazy functions")

    only_even = lambda xs: lazy_filter(lambda x: x % 2 == 0, xs)
    square_all = lambda xs: lazy_map(lambda x: x * x, xs)

    even_then_square = compose(square_all, only_even)
    result = even_then_square(range(1, 10))

    print("compose(square_all, only_even)(range(1, 10)):")
    for value in result:
        print(value)

    print(
        "\nПояснення:\n"
        "- compose(f, g) повертає нову функцію.\n"
        "- Спочатку виконується g(data), потім f(result).\n"
        "- Якщо обидві функції lazy, композиція теж lazy."
    )


# ---------------------------------------------------------------------------
# Завдання 17. Lazy reduce
# ---------------------------------------------------------------------------

def task_17_lazy_reduce() -> None:
    print_header("Завдання 17. Lazy reduce")

    data = lazy_map(debug, range(1, 6))
    deferred_sum = lazy_reduce(lambda acc, x: acc + x, data, 0)

    print("lazy_reduce створено. Processing ще не виводився.")
    print("Викликаємо deferred_sum():")

    result = deferred_sum()

    print(f"Result: {result}")

    print(
        "\nПояснення:\n"
        "- reduce є terminal operation.\n"
        "- Але через повернення compute() ми відкладаємо запуск обчислення.\n"
        "- Ітерація починається тільки при виклику deferred_sum()."
    )


# ---------------------------------------------------------------------------
# Завдання 18. Lazy Data Processing Engine
# ---------------------------------------------------------------------------

def task_18_lazy_data_processing_engine() -> None:
    print_header("Завдання 18. Lazy Data Processing Engine")

    data = range(1, 1_000_000)

    steps = [
        lambda xs: lazy_filter(lambda x: x % 3 == 0, xs),
        lambda xs: lazy_map(lambda x: x * x, xs),
        lambda xs: lazy_filter(lambda x: x > 100, xs),
    ]

    result = run_pipeline(data, steps)

    print(f"type(result) = {type(result)}")
    print("Перші 10 значень:")
    for value in take(10, result):
        print(value)

    print(
        "\nПояснення:\n"
        "- run_pipeline не створює списків.\n"
        "- Кожен step повертає lazy iterable.\n"
        "- Дані обчислюються тільки під час ітерації по result."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_selected_task(task_number: str) -> None:
    tasks: dict[str, Callable[[], None]] = {
        "1": task_1_eager_vs_lazy,
        "2": task_2_generator_with_yield,
        "3": task_3_lazy_square,
        "4": task_4_lazy_filter,
        "5": task_5_lazy_map,
        "6": task_6_combining_lazy_functions,
        "7": task_7_pipeline,
        "8": task_8_lazy_pipeline_first_5,
        "9": task_9_deferred_execution,
        "10": task_10_on_demand_with_next,
        "11": task_11_large_range,
        "12": task_12_read_lines_simulation,
        "13": task_13_transactions_de_style,
        "14": task_14_pipeline_logging,
        "15": task_15_infinite_sequence,
        "16": task_16_compose_lazy_functions,
        "17": task_17_lazy_reduce,
        "18": task_18_lazy_data_processing_engine,
    }

    if task_number == "all":
        for number in map(str, range(1, 19)):
            tasks[number]()
        return

    if task_number not in tasks:
        available = ", ".join(["all"] + list(tasks.keys()))
        raise ValueError(f"Невідоме завдання: {task_number}. Доступні варіанти: {available}")

    tasks[task_number]()


def main() -> None:
    parser = argparse.ArgumentParser(description="Завдання з Lazy Evaluation у Python")
    parser.add_argument(
        "--task",
        default="all",
        help="Номер завдання: 1..18 або all. За замовчуванням: all",
    )

    args = parser.parse_args()
    run_selected_task(args.task)


if __name__ == "__main__":
    main()
