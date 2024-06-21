from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Student, Attendance, StudentAttendanceSummary
from django.utils.dateparse import parse_date

@login_required
def take_and_view_attendance(request, group_id=None, date=None):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        date = request.POST.get('date')
        group = get_object_or_404(Group, id=group_id, instructor__employee__user=request.user)
        students = Student.objects.filter(group=group)

        attendance_data = request.POST.getlist('attendance')
        for student in students:
            is_present = str(student.id) in attendance_data
            Attendance.objects.update_or_create(
                date=parse_date(date),
                student=student,
                defaults={'present': is_present}
            )

        # Calculate the total present and absent days for each student
        for student in students:
            total_present = Attendance.objects.filter(student=student, present=True).count()
            total_absent = Attendance.objects.filter(student=student, present=False).count()
            StudentAttendanceSummary.objects.update_or_create(
                student=student,
                defaults={
                    'total_present_days': total_present,
                    'total_absent_days': total_absent
                }
            )

    else:
        group = None
        students = []

    groups = Group.objects.filter(instructor__employee__user=request.user)

    if group_id and date:
        group = get_object_or_404(Group, id=group_id, instructor__employee__user=request.user)
        students = Student.objects.filter(group=group)
        for student in students:
            total_present = Attendance.objects.filter(student=student, present=True).count()
            total_absent = Attendance.objects.filter(student=student, present=False).count()
            StudentAttendanceSummary.objects.update_or_create(
                student=student,
                defaults={
                    'total_present_days': total_present,
                    'total_absent_days': total_absent
                }
            )

    student_summaries = StudentAttendanceSummary.objects.filter(student__group=group) if group else []

    # Preparing student attendance data for the selected date
    student_attendance = {student.id: Attendance.objects.filter(student=student, date=parse_date(date)).first() if date else None for student in students}

    return render(request, 'attendance/take_and_view_attendance.html', {
        'groups': groups,
        'students': students,
        'group': group,
        'student_summaries': student_summaries,
        'date': date,
        'student_attendance': student_attendance,
    })
