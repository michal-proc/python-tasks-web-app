import tempfile
import importlib.util
import time
import ast

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render


def playground(request, form):
    if not form.is_valid():
        messages.error(request, "Form data is invalid.")
        return None

    user_code = form.cleaned_data['code']
    args = form.cleaned_data['args']
    expected = form.cleaned_data['expected']
    function_name = form.cleaned_data['function']

    # Parsing user data, should use try/except
    try:
        args_list = ast.literal_eval(f"[{args}]")
    except ValueError:
        messages.error(request, "Form arguments list is invalid.")
        return None

    # Parsing user data, should use try/except
    try:
        expected_list = ast.literal_eval(f"[{expected}]")
    except ValueError:
        messages.error(request, "Form expected data is invalid.")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as script_file:
        script_file.write(user_code)
        script_path = script_file.name

    # Parsing user data, should use try/except
    try:
        spec = importlib.util.spec_from_file_location("user_module", script_path)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        start_time = time.time()

        user_function = getattr(user_module, function_name)
        result = user_function(*args_list)

        end_time = time.time()
        execution_time = round(end_time - start_time, 3)

        if result in expected_list:
            output = {'result': 'Pass', 'execution_time': execution_time}
        else:
            output = {'result': 'Fail', 'actual_output': result,
                      'execution_time': execution_time}
    except Exception as error:
        output = {'error': str(error)}

    return output
