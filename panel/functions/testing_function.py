from django.core.files.storage import default_storage
from ..models import TestCase
import subprocess
import importlib.util
import time
import ast

from django.contrib import messages


def run_tests(request, solution):
    test_cases = TestCase.objects.filter(task=solution.task)
    results = {}

    for test_case in test_cases:
        # Parsing user data, should use try/except
        try:
            args_list = ast.literal_eval(f"[{test_case.input_data}]")
        except ValueError:
            messages.error(request, "Arguments list is invalid.")
            return None

        # Parsing user data, should use try/except
        try:
            expected_list = ast.literal_eval(f"[{test_case.expected_output}]")
        except ValueError:
            messages.error(request, "Form expected data is invalid.")
            return None

        # Parsing user data, should use try/except
        try:
            spec = importlib.util.spec_from_file_location("user_module", solution.solution_file.path)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            start_time = time.time()

            user_function = getattr(user_module, "f")
            result = user_function(*args_list)

            end_time = time.time()
            execution_time = round(end_time - start_time, 3)

            if result in expected_list:
                results[test_case.id] = {'result': 'Pass', 'actual_output': result, 'expected_output': expected_list,
                                         'execution_time': execution_time}
            else:
                results[test_case.id] = {'result': 'Fail', 'actual_output': result, 'expected_output': expected_list,
                                         'execution_time': execution_time}
        except Exception as error:
            results[test_case.id] = {'result': 'Fail', 'error': str(error)}

    return results
