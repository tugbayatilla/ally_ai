import pytest
import logging
import re
import asyncio

from lib.core.ally_ai_core.decorators import timed

# Configure a logger for testing if needed
logger = logging.getLogger(__name__)

# ---------------------------
# Helper Functions for Testing
# ---------------------------


# Sample synchronous functions
@timed
def add(a, b):
    """Adds two numbers."""
    return a + b


@timed(message="Adding numbers", level=logging.DEBUG)
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b


@timed
def greet(name: str) -> str:
    """Greets a person."""
    return f"Hello, {name}!"


# Sample asynchronous functions
@timed
async def async_add(a, b):
    """Asynchronously adds two numbers."""
    await asyncio.sleep(0.1)
    return a + b


@timed(message="Async multiplying numbers", level=logging.WARNING)
async def async_multiply(a, b):
    """Asynchronously multiplies two numbers."""
    await asyncio.sleep(0.1)
    return a * b


# Function that raises an exception
@timed
def divide(a, b):
    """Divides two numbers."""
    return a / b


@timed
async def async_divide(a, b):
    """Asynchronously divides two numbers."""
    await asyncio.sleep(0.1)
    return a / b


# Function with various arguments
@timed
def complex_function(a, b=2, *args, **kwargs):
    """Function with various arguments."""
    return a + b + sum(args) + sum(kwargs.values())


# ---------------------------
# Test Cases
# ---------------------------


# 1. Test synchronous function without decorator arguments
def test_timed_add(caplog):
    with caplog.at_level(logging.INFO):
        result = add(2, 3)
        assert result == 5, "add function should return the sum of two numbers"

        # Check that a log message was emitted
        assert any(
            "add took" in record.message for record in caplog.records
        ), "No log message contains 'add took'"

        # Verify the log message format using regex
        pattern = r"Timed: add took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 2. Test synchronous function with decorator arguments
def test_timed_multiply(caplog):
    with caplog.at_level(logging.DEBUG):
        result = multiply(3, 4)
        assert (
            result == 12
        ), "multiply function should return the product of two numbers"

        # Check that a log message was emitted with the custom message
        assert any(
            "Adding numbers - multiply took" in record.message
            for record in caplog.records
        ), "No log message contains 'Adding numbers - multiply took'"

        # Verify the log message format using regex
        pattern = r"Timed: Adding numbers - multiply took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 3. Test asynchronous function without decorator arguments
@pytest.mark.asyncio
async def test_timed_async_add(caplog):
    with caplog.at_level(logging.INFO):
        result = await async_add(5, 7)
        assert result == 12, "async_add function should return the sum of two numbers"

        # Check that a log message was emitted
        assert any(
            "async_add took" in record.message for record in caplog.records
        ), "No log message contains 'async_add took'"

        # Verify the log message format using regex
        pattern = r"Timed: async_add took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 4. Test asynchronous function with decorator arguments
@pytest.mark.asyncio
async def test_timed_async_multiply(caplog):
    with caplog.at_level(logging.WARNING):
        result = await async_multiply(6, 7)
        assert (
            result == 42
        ), "async_multiply function should return the product of two numbers"

        # Check that a log message was emitted with the custom message
        assert any(
            "Async multiplying numbers - async_multiply took" in record.message
            for record in caplog.records
        ), "No log message contains 'Async multiplying numbers - async_multiply took'"

        # Verify the log message format using regex
        pattern = r"Timed: Async multiplying numbers - async_multiply took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 5. Test decorator on function that raises an exception (synchronous)
def test_timed_divide_exception(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Even if the function raises, the decorator should log the elapsed time
        assert any(
            "divide took" in record.message for record in caplog.records
        ), "No log message contains 'divide took'"

        # Verify the log message format using regex
        pattern = r"Timed: divide took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 6. Test decorator on function that raises an exception (asynchronous)
@pytest.mark.asyncio
async def test_timed_async_divide_exception(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            await async_divide(10, 0)

        # Even if the function raises, the decorator should log the elapsed time
        assert any(
            "async_divide took" in record.message for record in caplog.records
        ), "No log message contains 'async_divide took'"

        # Verify the log message format using regex
        pattern = r"Timed: async_divide took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 7. Test decorator preserves function metadata (__name__, __doc__)
def test_timed_metadata():
    assert add.__name__ == "add", "Decorator should preserve the function name"
    assert (
        add.__doc__ == "Adds two numbers."
    ), "Decorator should preserve the function docstring"

    assert (
        multiply.__name__ == "multiply"
    ), "Decorator should preserve the function name"
    assert (
        multiply.__doc__ == "Multiplies two numbers."
    ), "Decorator should preserve the function docstring"

    assert (
        async_add.__name__ == "async_add"
    ), "Decorator should preserve the function name"
    assert (
        async_add.__doc__ == "Asynchronously adds two numbers."
    ), "Decorator should preserve the function docstring"

    assert (
        async_multiply.__name__ == "async_multiply"
    ), "Decorator should preserve the function name"
    assert (
        async_multiply.__doc__ == "Asynchronously multiplies two numbers."
    ), "Decorator should preserve the function docstring"


# 8. Test decorator on function with various arguments
def test_timed_complex_function(caplog):
    with caplog.at_level(logging.INFO):
        result = complex_function(1, 3, 5, 7, x=9, y=11)
        assert (
            result == 1 + 3 + 5 + 7 + 9 + 11
        ), "complex_function should correctly sum all arguments"

        # Check that a log message was emitted
        assert any(
            "complex_function took" in record.message for record in caplog.records
        ), "No log message contains 'complex_function took'"

        # Verify the log message format using regex
        pattern = r"Timed: complex_function took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 9. Test decorator used without arguments vs. with arguments
def test_timed_decorator_usage(caplog):
    with caplog.at_level(logging.DEBUG):
        # Function decorated without arguments
        result_add = add(4, 5)
        assert result_add == 9, "add function should return the sum of two numbers"

        # Function decorated with arguments
        result_multiply = multiply(4, 5)
        assert (
            result_multiply == 20
        ), "multiply function should return the product of two numbers"

        # Check log messages
        assert any(
            "add took" in record.message for record in caplog.records
        ), "No log message contains 'add took'"

        assert any(
            "Adding numbers - multiply took" in record.message
            for record in caplog.records
        ), "No log message contains 'Adding numbers - multiply took'"


# 10. Test decorator with different logging levels
def test_timed_logging_levels(caplog):
    with caplog.at_level(logging.DEBUG):
        multiply(2, 3)  # Decorated with DEBUG level
        add(2, 3)  # Decorated with INFO level

        # Check that multiply logs at DEBUG level
        debug_logs = [
            record for record in caplog.records if record.levelno == logging.DEBUG
        ]
        assert any(
            "Adding numbers - multiply took" in record.message for record in debug_logs
        ), "No DEBUG level log contains 'Adding numbers - multiply took'"

        # Check that add logs at INFO level
        info_logs = [
            record for record in caplog.records if record.levelno == logging.INFO
        ]
        assert any(
            "add took" in record.message for record in info_logs
        ), "No INFO level log contains 'add took'"


# 11. Test multiple decorations on the same function
@timed(message="First decorator", level=logging.INFO)
@timed(message="Second decorator", level=logging.DEBUG)
def double(a):
    """Doubles a number."""
    return a * 2


def test_timed_multiple_decorators(caplog):
    with caplog.at_level(logging.DEBUG):
        result = double(5)
        assert result == 10, "double function should return twice the input"

        # Expect two log messages due to multiple decorators
        first_log = "Timed: First decorator - double took"
        second_log = "Timed: Second decorator - double took"

        # Check for both log messages
        assert any(
            first_log in record.message for record in caplog.records
        ), "No log message contains both decorators' messages"

        assert any(
            second_log in record.message for record in caplog.records
        ), "No log message contains 'Second decorator - double took'"


# 12. Test decorator with functions returning different types
def test_timed_various_return_types(caplog):
    with caplog.at_level(logging.INFO):
        # Function returning string
        greeting = greet("Alice")
        assert (
            greeting == "Hello, Alice!"
        ), "greet function should return a greeting string"

        # Function returning integer
        result_add = add(10, 20)
        assert result_add == 30, "add function should return the sum of two numbers"

        # Check log messages
        assert any(
            "greet took" in record.message for record in caplog.records
        ), "No log message contains 'greet took'"

        assert any(
            "add took" in record.message for record in caplog.records
        ), "No log message contains 'add took'"


# 13. Test decorator with no return (void function)
@timed
def void_function():
    """Function that returns nothing."""
    pass


def test_timed_void_function(caplog):
    with caplog.at_level(logging.INFO):
        result = void_function()
        assert result is None, "void_function should return None"

        # Check that a log message was emitted
        assert any(
            "void_function took" in record.message for record in caplog.records
        ), "No log message contains 'void_function took'"

        # Verify the log message format using regex
        pattern = r"Timed: void_function took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 14. Test decorator with functions having no arguments
@timed
def no_args_function():
    """Function that takes no arguments."""
    return "No args"


def test_timed_no_args_function(caplog):
    with caplog.at_level(logging.INFO):
        result = no_args_function()
        assert result == "No args", "no_args_function should return 'No args'"

        # Check that a log message was emitted
        assert any(
            "no_args_function took" in record.message for record in caplog.records
        ), "No log message contains 'no_args_function took'"

        # Verify the log message format using regex
        pattern = r"Timed: no_args_function took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 15. Test decorator with functions having keyword-only arguments
@timed
def keyword_only_function(a, *, b=10):
    """Function with keyword-only arguments."""
    return a + b


def test_timed_keyword_only_function(caplog):
    with caplog.at_level(logging.INFO):
        result = keyword_only_function(5, b=15)
        assert (
            result == 20
        ), "keyword_only_function should correctly handle keyword-only arguments"

        # Check that a log message was emitted
        assert any(
            "keyword_only_function took" in record.message for record in caplog.records
        ), "No log message contains 'keyword_only_function took'"

        # Verify the log message format using regex
        pattern = r"Timed: keyword_only_function took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# ---------------------------
# Additional Test Cases (Optional)
# ---------------------------


# 16. Test decorator on method within a class
class SampleClass:
    @timed
    def method_add(self, a, b):
        """Method that adds two numbers."""
        return a + b

    @timed(message="Method multiply", level=logging.ERROR)
    async def async_method_multiply(self, a, b):
        """Asynchronous method that multiplies two numbers."""
        await asyncio.sleep(0.1)
        return a * b


def test_timed_class_methods(caplog):
    with caplog.at_level(logging.INFO):
        instance = SampleClass()
        result = instance.method_add(7, 8)
        assert result == 15, "method_add should return the sum of two numbers"

        # Check that a log message was emitted
        assert any(
            "method_add took" in record.message for record in caplog.records
        ), "No log message contains 'method_add took'"

        # Verify the log message format using regex
        pattern = r"Timed: method_add took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


@pytest.mark.asyncio
async def test_timed_async_class_methods(caplog):
    with caplog.at_level(logging.ERROR):
        instance = SampleClass()
        result = await instance.async_method_multiply(3, 4)
        assert (
            result == 12
        ), "async_method_multiply should return the product of two numbers"

        # Check that a log message was emitted with the custom message and ERROR level
        error_logs = [
            record for record in caplog.records if record.levelno == logging.ERROR
        ]
        assert any(
            "Method multiply - async_method_multiply took" in record.message
            for record in error_logs
        ), "No ERROR level log contains 'Method multiply - async_method_multiply took'"

        # Verify the log message format using regex
        pattern = r"Timed: Method multiply - async_method_multiply took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in error_logs
        ), "No log message matches the expected pattern."


# 17. Test decorator on lambda function
# Note: Decorating lambda functions is uncommon and might not preserve metadata as expected
@timed
def decorated_lambda():
    """Function returning a lambda."""
    return lambda x: x * x


def test_timed_lambda_function(caplog):
    with caplog.at_level(logging.INFO):
        lambda_func = decorated_lambda()
        assert (
            lambda_func(5) == 25
        ), "Lambda function should return the square of the input"

        # Check that a log message was emitted
        assert any(
            "decorated_lambda took" in record.message for record in caplog.records
        ), "No log message contains 'decorated_lambda took'"

        # Verify the log message format using regex
        pattern = r"Timed: decorated_lambda took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 18. Test decorator with functions having default mutable arguments
@timed
def append_to_list(item, lst=None):
    """Function that appends an item to a list."""
    if lst is None:
        lst = []
    lst.append(item)
    return lst


def test_timed_default_mutable_arguments(caplog):
    with caplog.at_level(logging.INFO):
        result1 = append_to_list(1)
        result2 = append_to_list(2)

        assert result1 == [1], "First call should return [1]"
        assert result2 == [
            2
        ], "Second call should return [2], ensuring no shared mutable default"

        # Check that two log messages were emitted
        assert (
            len(
                [
                    record
                    for record in caplog.records
                    if "append_to_list took" in record.message
                ]
            )
            == 2
        ), "Two log messages should be emitted for two function calls"


# 19. Test decorator on generator function
@timed
def generator_function(n):
    """Generator that yields numbers up to n."""
    for i in range(n):
        yield i


def test_timed_generator_function(caplog):
    with caplog.at_level(logging.INFO):
        gen = generator_function(3)
        result = list(gen)
        assert result == [
            0,
            1,
            2,
        ], "generator_function should yield numbers from 0 to n-1"

        # Since generator_function is a generator, the decorator logs after the generator is created, not after iteration
        assert any(
            "generator_function took" in record.message for record in caplog.records
        ), "No log message contains 'generator_function took'"

        # Verify the log message format using regex
        pattern = r"Timed: generator_function took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."


# 20. Test decorator on class constructor (__init__)
class ClassWithInit:
    @timed
    def __init__(self, value):
        """Constructor that initializes the value."""
        self.value = value


def test_timed_class_constructor(caplog):
    with caplog.at_level(logging.INFO):
        obj = ClassWithInit(10)
        assert obj.value == 10, "ClassWithInit should correctly initialize the value"

        # Check that a log message was emitted for __init__
        assert any(
            "__init__ took" in record.message for record in caplog.records
        ), "No log message contains '__init__ took'"

        # Verify the log message format using regex
        pattern = r"Timed: __init__ took \d+\.\d{6} seconds to finish"
        assert any(
            re.match(pattern, record.message) for record in caplog.records
        ), "No log message matches the expected pattern."
