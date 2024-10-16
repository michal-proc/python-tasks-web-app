from ..forms.group_form import GroupForm
import uuid


def create_group(form_data, user, files=None):
    form = GroupForm(form_data, files)
    if form.is_valid():
        group = form.save(commit=False)
        group.creator = user

        if not group.join_code:
            group.join_code = str(uuid.uuid4())[:12]
        if not group.join_code_for_instructor:
            group.join_code_for_instructor = str(uuid.uuid4())[:12]

        group.save()
        return group
    else:
        print(form.errors)
        return None
