from django.contrib import admin
from .models import (
    DisasterType, EducationModule, Quiz, QuizQuestion, DrillChecklist, DrillStep,
    UserProfile, ModuleProgress, QuizAttempt, DrillCompletion, EmergencyContact
)

@admin.register(DisasterType)
class DisasterTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']

class EducationModuleInline(admin.TabularInline):
    model = EducationModule
    extra = 1
    fields = ['title', 'order', 'estimated_read_time']

@admin.register(EducationModule)
class EducationModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'disaster_type', 'order', 'estimated_read_time', 'created_at']
    list_filter = ['disaster_type', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['disaster_type', 'order']

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = ['question_text', 'correct_answer', 'order']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'disaster_type', 'created_at']
    list_filter = ['disaster_type', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuizQuestionInline]

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer', 'order']
    list_filter = ['quiz__disaster_type', 'correct_answer']
    search_fields = ['question_text']

class DrillStepInline(admin.TabularInline):
    model = DrillStep
    extra = 1
    fields = ['step_text', 'order', 'is_critical', 'time_limit']

@admin.register(DrillChecklist)
class DrillChecklistAdmin(admin.ModelAdmin):
    list_display = ['title', 'disaster_type', 'created_at']
    list_filter = ['disaster_type', 'created_at']
    search_fields = ['title', 'description']
    inlines = [DrillStepInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'institution', 'grade_level', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'institution']

@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'completed', 'completion_date', 'time_spent']
    list_filter = ['completed', 'module__disaster_type', 'completion_date']
    search_fields = ['user__username', 'module__title']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'correct_answers', 'total_questions', 'completed_at']
    list_filter = ['quiz__disaster_type', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['completed_at']

@admin.register(DrillCompletion)
class DrillCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'drill_checklist', 'completion_percentage', 'completed_at']
    list_filter = ['drill_checklist__disaster_type', 'completed_at']
    search_fields = ['user__username', 'drill_checklist__title']
    readonly_fields = ['completed_at']

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'phone_number', 'contact_type', 'is_active']
    list_filter = ['contact_type', 'is_active', 'created_at']
    search_fields = ['name', 'organization', 'phone_number']
