from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

User = get_user_model()

# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "last_login",
        "phone_no",
    )
    list_filter = ("is_admin",)
    # To control the layout of admin "add" or "change" pages
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_staff",
                    # "is_superuser",
                    # "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Contact info", {"fields": ("phone_no",)}),
    )
    # For creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    filter_horizontal = ()
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)


admin.site.register(User, UserAdmin)
