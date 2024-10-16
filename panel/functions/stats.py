from panel.models import Solution


def count_stats(solutions):
    stats = {
        'solutions_number': len(solutions),
        'tests_number': 0,
        'tests_passed': 0,
        'tests_failed': 0,
        'average_test_time': 0,
        'total_time': 0,
    }
    results = []
    if len(solutions) == 0:
        return stats
    for solution in solutions:
        for value in solution.test_results.values():
            results.append(value)

    for result in results:
        if 'result' in result and result['result'] == 'Pass':
            stats['tests_passed'] += 1
        else:
            stats['tests_failed'] += 1

        if 'execution_time' in result:
            stats['total_time'] += result['execution_time']

    stats['tests_number'] = stats['tests_failed'] + stats['tests_passed']
    stats['average_test_time'] = stats['total_time'] / stats['tests_number']
    return stats


def count_table(task):
    # Reverse, because we analyze only last solution
    all_solutions = Solution.objects.filter(task=task).order_by('-submitted_at')
    user_stats = {}

    for solution in all_solutions:
        user = solution.user
        if user not in user_stats:
            user_stats[user] = {
                'solution_id': solution.id, 'user_mail': user.email, 'username': user.username, 'tests_passed': 0,
                'tests': 0, 'total_time': 0.0, 'points': solution.points}

            for test_result in solution.test_results.values():
                user_stats[user]['tests'] += 1
                if test_result.get('result') == 'Pass':
                    user_stats[user]['tests_passed'] += 1
                    user_stats[user]['total_time'] += test_result.get('execution_time', 0.0)

    ranking_table = sorted(user_stats.items(), key=lambda item: (-item[1]['tests_passed'], item[1]['total_time']))

    return ranking_table
