import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق حسو ال علي"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#f0f4f8"
    page.padding = 40

    def show_login_view(e=None):
        # تنظيف الصفحة وإظهار واجهة تسجيل الدخول
        page.clean()
        page.add(login_view)

    def show_register_view(e=None):
        # تنظيف الصفحة وإظهار واجهة إنشاء الحساب
        page.clean()
        page.add(register_view)

    def create_text_field(label, hint_text="", password=False):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            password=password,
            width=300,
            border_radius=10,
            filled=True,
            bgcolor="#ffffff",
            content_padding=ft.Padding(15, 15, 15, 15),
            text_style=ft.TextStyle(size=14),
        )

    # واجهة تسجيل الدخول
    login_view = ft.Column(
        [
            ft.Text("تسجيل الدخول", size=24, weight="bold", color="#4A90E2"),
            create_text_field("البريد الإلكتروني", hint_text="example@mail.com"),
            create_text_field("كلمة المرور", password=True),
            ft.ElevatedButton("تسجيل الدخول", width=300, bgcolor="#4A90E2", color="white"),
            ft.TextButton("إنشاء حساب جديد", on_click=show_register_view, style=ft.ButtonStyle(color="#4A90E2")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # واجهة إنشاء الحساب
    register_view = ft.Column(
        [
            ft.Text("إنشاء حساب", size=24, weight="bold", color="#4A90E2"),
            create_text_field("اسم المستخدم", hint_text="@username"),
            create_text_field("البريد الإلكتروني", hint_text="xxxxx@mail.com"),
            create_text_field("رقم الهاتف", hint_text="+96478xxxxxxxxx"),
            create_text_field("الاسم الكامل", hint_text="مثل : حسو ال علي"),
            create_text_field("كلمة المرور", password=True),
            ft.ElevatedButton("إنشاء حساب", width=300, bgcolor="#4A90E2", color="white"),
            ft.TextButton("لديك حساب؟ سجل دخولك", on_click=show_login_view, style=ft.ButtonStyle(color="#4A90E2")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # عرض واجهة تسجيل الدخول كافتراضية عند تشغيل التطبيق
    show_login_view()

ft.app(target=main)
