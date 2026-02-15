from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db.models import Count
from .models import Student, Attendance
from django.db.models import OuterRef, Subquery

# ================= HELPER =================
def is_admin(user):
    return user.is_staff


# ================= USER DASHBOARD (READ ONLY) =================
@login_required
def dashboard(request):
    query = request.GET.get("q")

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    # Get latest attendance for each student
    latest_attendance = Attendance.objects.filter(
        student=OuterRef("pk")
    ).order_by("-date")

    students = students.annotate(
        latest_status=Subquery(latest_attendance.values("status")[:1])
    )

    return render(request, "dashboard.html", {
        "students": students,
        "query": query
    })

# ================= ADMIN DASHBOARD =================
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    query = request.GET.get("q")

    students_list = Student.objects.all().order_by("-id")

    if query:
        students_list = students_list.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )

    paginator = Paginator(students_list, 5)
    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

    return render(request, "admin_dashboard.html", {
        "students": students,   # ✅ MUST be students
        "query": query
    })



# ================= ADD STUDENT =================
@login_required
@user_passes_test(is_admin)
def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        department = request.POST.get("department")
        year = request.POST.get("year")
        photo = request.FILES.get("photo")

        # Duplicate email check
        if Student.objects.filter(email=email).exists():
            messages.error(request, "⚠ Email already exists!")
            return render(request, "add_student.html")

        Student.objects.create(
            name=name,
            email=email,
            department=department,
            year=year,
            photo=photo
        )

        messages.success(request, "✅ Student added successfully!")
        return redirect("students:admin_dashboard")

    return render(request, "add_student.html")


# ================= UPDATE STUDENT =================
@login_required
@user_passes_test(is_admin)
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.department = request.POST.get("department")
        student.year = request.POST.get("year")

        if request.FILES.get("photo"):
            student.photo = request.FILES.get("photo")

        student.save()
        messages.success(request, "✏ Student updated successfully!")
        return redirect("students:admin_dashboard")

    return render(request, "update_student.html", {
        "student": student
    })


# ================= DELETE STUDENT =================
@login_required
@user_passes_test(is_admin)
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "🗑 Student deleted successfully!")
    return redirect("students:admin_dashboard")


# ================= MARK ATTENDANCE =================
@login_required
@user_passes_test(is_admin)
def mark_attendance(request, id):
    student = get_object_or_404(Student, id=id)

    # Save attendance
    if request.method == "POST":
        status = request.POST.get("status")
        Attendance.objects.create(
            student=student,
            status=status
        )
        return redirect("students:attendance", id=id)


    # Attendance history
    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by("-id")

    total_classes = attendance_records.count()
    present_count = attendance_records.filter(status="Present").count()

    percentage = 0
    if total_classes > 0:
        percentage = int((present_count / total_classes) * 100)

    context = {
        "student": student,
        "attendance_records": attendance_records,
        "total_classes": total_classes,
        "present_count": present_count,
        "percentage": percentage,
    }

    return render(request, "attendance.html", context)

# ================= EXPORT PDF =================
@login_required
@user_passes_test(is_admin)
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response)
    y = 800

    students = Student.objects.all().order_by("-id")

    for student in students:
        p.drawString(
            100,
            y,
            f"{student.name} - {student.email} - {student.department}"
        )
        y -= 20

    p.save()
    return response


# ================= CHART DASHBOARD =================
@login_required
@user_passes_test(is_admin)
def chart_dashboard(request):

    total_students = Student.objects.count()

    department_data = list(
        Student.objects
        .values("department")
        .annotate(count=Count("id"))
        .order_by("department")
    )

    year_data = list(
        Student.objects
        .values("year")
        .annotate(count=Count("id"))
        .order_by("year")
    )

    return render(request, "chart_dashboard.html", {
        "total_students": total_students,
        "department_data": department_data,  # ✅ NOW LIST
        "year_data": year_data,              # ✅ NOW LIST
    })
