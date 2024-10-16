from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from panel.controllers import group_controller
from panel.enums.role import Role
from panel.forms.group_form import GroupForm, GroupMessageForm
from panel.forms.join_group_as_instructor_form import JoinGroupAsInstructorForm
from panel.forms.join_group_as_student_form import JoinGroupAsStudentForm
from panel.forms.task_form import TaskForm
from panel.models import Group, task, Task
from panel.models.group import GroupMembership, GroupMessage


@login_required
def view_group(request, group_id):
    user = request.user
    group = Group.objects.get(pk=group_id)
    task_form = TaskForm()

    if user.id == group.creator.id:
        return render(request, 'panel/groups/group_owner.html', {'group': group, 'task_form': task_form})

    membership = GroupMembership.objects.filter(group=group, user=user).first()
    if membership:
        if membership.role == 'INSTRUCTOR':
            return render(request, 'panel/groups/group_instructor.html', {'group': group, 'task_form': task_form})
        elif membership.role == 'STUDENT':
            return render(request, 'panel/groups/group_student.html', {'group': group, 'task_form': task_form})

    messages.error(request, 'You do not belong to this group.')
    return redirect('dashboard')


@login_required
@require_http_methods(["POST"])
def create_group_task(request, group_id):
    group = Group.objects.get(pk=group_id)
    task_form = TaskForm(request.POST)
    if task_form.is_valid():
        task = task_form.save(commit=False)
        task.creator = request.user
        task.group = group
        task.save()
        messages.info(request, "Task created successfully.")
    else:
        messages.error(request, "Error updating task.")

    return redirect('view_group', group_id=group.id)


@login_required
@require_http_methods(["POST"])
def delete_group_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    group_id = task.group.id
    task.delete()
    messages.info(request, 'Task has been deleted successfully.')
    return redirect('view_group', group_id=group_id)


@login_required
@require_http_methods(["POST"])
def create_group_message(request, group_id):
    group = Group.objects.get(pk=group_id)

    form = GroupMessageForm(request.POST, request.FILES)
    if form.is_valid():
        group_message = form.save(commit=False)
        group_message.group = group
        group_message.user = request.user
        group_message.save()
        messages.info(request, 'Message has been created successfully.')
    else:
        messages.error(request, 'There was an error creating the message.')

    return redirect('view_group', group_id=group.id)


@login_required
@require_http_methods(["POST"])
def delete_group_message(request, message_id):
    message = GroupMessage.objects.get(pk=message_id)
    group_id = message.group.id
    message.delete()
    messages.info(request, 'Message has been deleted successfully.')
    return redirect('view_group', group_id=group_id)


@login_required
@require_http_methods(["POST"])
def delete_group_member(request, group_id, user_id):
    group = Group.objects.get(pk=group_id)
    member = GroupMembership.objects.get(group=group, user_id=user_id)
    member.delete()
    messages.success(request, "Member has been deleted successfully.")
    return redirect('view_group', group_id=group_id)


@login_required
def create(request):
    form = GroupForm()
    if request.method == 'POST':
        new_group = group_controller.create_group(request.POST, request.user, request.FILES)
        if new_group:
            messages.info(request, 'New group created')
            return redirect('dashboard')

        messages.error(request, 'Cannot create a new group')
        form = GroupForm(request.POST, request.FILES)

    return render(request, 'panel/create_group.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def update(request, group_id):
    group = Group.objects.get(pk=group_id)
    group_form = GroupForm(request.POST, request.FILES, instance=group)
    if group_form.is_valid():
        group_form.save()
        messages.info(request, "Group updated successfully.")
    else:
        messages.error(request, "Error updating group.")

    return redirect('view_group', group_id=group.id)


@login_required
def delete(request, group_id):
    group = Group.objects.get(pk=group_id)
    group.delete()
    messages.info(request, 'Group has been deleted successfully.')
    return redirect('my_groups')


@login_required
@require_http_methods(["POST"])
def delete_group_image(request, group_id):
    group = Group.objects.get(pk=group_id)

    if request.user != group.creator:
        messages.error(request, "You do not have permission to delete this image.")
        return redirect('view_group', group_id=group.id)

    group.image.delete()
    group.save()
    messages.success(request, "Group image deleted successfully.")
    return redirect('view_group', group_id=group.id)


@login_required
def join_group(request):
    student_form = JoinGroupAsStudentForm()
    instructor_form = JoinGroupAsInstructorForm()
    return render(request, 'panel/join_group.html', {'student_form': student_form, 'instructor_form': instructor_form})


@login_required
@require_http_methods(["POST"])
def join_group_as_student(request):
    form = JoinGroupAsStudentForm(request.POST)
    if form.is_valid():
        join_code = form.cleaned_data['join_code_student']
        group = Group.objects.filter(join_code=join_code).first()
        if group and request.user is not group.creator:
            GroupMembership.objects.create(group=group, user=request.user, role=Role.STUDENT)
            messages.info(request, 'You have successfully joined the group as a student')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid join code for student')
    else:
        messages.error(request, 'Invalid form submission')
    return redirect('join_group')


@login_required
@require_http_methods(["POST"])
def quit_group(request, group_id):
    user = request.user
    group = Group.objects.get(pk=group_id)

    membership = GroupMembership.objects.filter(group=group, user=user).first()
    membership.delete()
    messages.info(request, 'You have successfully quit the group.')

    return redirect('dashboard')


@login_required
@require_http_methods(["POST"])
def join_group_as_instructor(request):
    form = JoinGroupAsInstructorForm(request.POST)
    if form.is_valid():
        join_code = form.cleaned_data['join_code_instructor']
        group = Group.objects.filter(join_code_for_instructor=join_code).first()
        if group is not group.creator:
            GroupMembership.objects.create(group=group, user=request.user, role=Role.INSTRUCTOR)
            messages.info(request, 'You have successfully joined the group as an instructor')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid join code for instructor')
    else:
        messages.error(request, 'Invalid form submission')
    return redirect('join_group')


@login_required
def my_groups(request):
    user = request.user

    role_filter = request.GET.get('role')
    user_filter = request.GET.get('user')
    group_name_filter = request.GET.get('group_name')

    created_groups = Group.objects.filter(creator=user)
    instructor_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.INSTRUCTOR)
    student_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.STUDENT)

    groups_with_roles = []

    for group in created_groups:
        groups_with_roles.append({'group': group, 'role': 'OWNER'})

    for group in instructor_groups:
        groups_with_roles.append({'group': group, 'role': 'INSTRUCTOR'})

    for group in student_groups:
        groups_with_roles.append({'group': group, 'role': 'STUDENT'})

    if role_filter:
        groups_with_roles = [g for g in groups_with_roles if g['role'] == role_filter.upper()]

    if user_filter:
        groups_with_roles = [g for g in groups_with_roles if
                             user_filter.lower() in g['group'].creator.get_full_name().lower()]

    if group_name_filter:
        groups_with_roles = [g for g in groups_with_roles if group_name_filter.lower() in g['group'].name.lower()]

    return render(request, 'panel/my_groups.html', {'title': 'My Groups', 'groups_with_roles': groups_with_roles})
