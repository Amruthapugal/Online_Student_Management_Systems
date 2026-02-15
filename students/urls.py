from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add/", views.add_student, name="add_student"),
    path("update/<int:id>/", views.update_student, name="update_student"),
    path("delete/<int:id>/", views.delete_student, name="delete_student"),
    path("attendance/<int:id>/", views.mark_attendance, name="attendance"),
    path("charts/", views.chart_dashboard, name="charts"),  # ✅ THIS IS IMPORTANT
    path("export-pdf/", views.export_pdf, name="export_pdf"),
]
