from django.urls import path

from .views import dashboard_views, task_views, solutions_views, group_views, plagiarism_views, account_settings_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),

    path('group/create', group_views.create, name='group_create'),

    path('groups/mine', group_views.my_groups, name='my_groups'),

    path('groups/<int:group_id>', group_views.view_group, name='view_group'),
    path('groups/<int:group_id>/update', group_views.update, name='update_group'),
    path('groups/<int:group_id>/delete', group_views.delete, name='delete_group'),
    path('group/<int:group_id>/delete-image/', group_views.delete_group_image, name='delete_group_image'),
    path('quit-group/<int:group_id>/', group_views.quit_group, name='quit_group'),
    path('group/<int:group_id>/create-task/', group_views.create_group_task, name='create_task'),
    path('group/<int:task_id>/delete-task/', group_views.delete_group_task, name='delete_task'),
    path('group/<int:group_id>/create-message/', group_views.create_group_message, name='create_group_message'),
    path('group/<int:message_id>/delete-message/', group_views.delete_group_message, name='delete_group_message'),
    path('group/<int:group_id>/delete-group-member/<int:user_id>', group_views.delete_group_member,
         name='delete_group_member'),

    path('join-group/', group_views.join_group, name='join_group'),
    path('join-group-as-student/', group_views.join_group_as_student, name='join_group_as_student'),
    path('join-group-as-instructor/', group_views.join_group_as_instructor, name='join_group_as_instructor'),

    path('show-solution/<int:solution_id>/', solutions_views.show_solution, name='solution'),
    path('submit-solution/<int:task_id>/', solutions_views.submit_solution, name='submit_solution'),
    path('update-points/<int:solution_id>/', solutions_views.update_points, name='update_points'),

    path('tasks/', task_views.view_tasks, name='view_tasks'),
    path('update-task/<int:task_id>/', task_views.update_task, name='update_task'),
    path('add-test-case/<int:task_id>/', task_views.add_test_case, name='add_test_case'),
    path('delete-test-case/<int:test_case_id>/', task_views.delete_test_case, name='delete_test_case'),

    path('check-plagiarism/<int:task_id>/', plagiarism_views.check_plagiarism, name='check_plagiarism'),
    path('show-plagiarism/<int:task_id>/', plagiarism_views.show_plagiarism, name='show_plagiarism'),

    path('account-settings/', account_settings_views.account_settings, name='account_settings'),
    path('account-settings/update-email/', account_settings_views.update_email, name='update_email'),
    path('account-settings/update-password/', account_settings_views.update_password, name='update_password'),
]
