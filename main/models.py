from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class DisasterType(models.Model):
    """Model for different types of disasters"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='⚠️')  # Emoji or icon class
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class EducationModule(models.Model):
    """Model for educational modules about disasters"""
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    estimated_read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.disaster_type.name} - {self.title}"
    
    class Meta:
        ordering = ['disaster_type', 'order']
        unique_together = ['disaster_type', 'order']

class Quiz(models.Model):
    """Model for quizzes related to disaster modules"""
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.disaster_type.name} Quiz - {self.title}"
    
    class Meta:
        verbose_name_plural = "Quizzes"

class QuizQuestion(models.Model):
    """Model for quiz questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D')
    ])
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"
    
    class Meta:
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']

class DrillChecklist(models.Model):
    """Model for virtual drill checklists"""
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE, related_name='drill_checklists')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.disaster_type.name} Drill - {self.title}"

class DrillStep(models.Model):
    """Model for individual steps in a drill checklist"""
    drill_checklist = models.ForeignKey(DrillChecklist, on_delete=models.CASCADE, related_name='steps')
    step_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_critical = models.BooleanField(default=False, help_text="Mark as critical step")
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Time limit in seconds")
    
    def __str__(self):
        return f"{self.drill_checklist.title} - Step {self.order}"
    
    class Meta:
        ordering = ['drill_checklist', 'order']
        unique_together = ['drill_checklist', 'order']

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator')
    ], default='student')
    institution = models.CharField(max_length=200, blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class ModuleProgress(models.Model):
    """Track user progress through education modules"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(EducationModule, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    time_spent = models.PositiveIntegerField(default=0, help_text="Time spent in seconds")
    
    def __str__(self):
        return f"{self.user.username} - {self.module.title}"
    
    class Meta:
        unique_together = ['user', 'module']

class QuizAttempt(models.Model):
    """Track user quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds")
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}%"
    
    class Meta:
        ordering = ['-completed_at']

class DrillCompletion(models.Model):
    """Track user drill completions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drill_checklist = models.ForeignKey(DrillChecklist, on_delete=models.CASCADE)
    completed_steps = models.PositiveIntegerField(default=0)
    total_steps = models.PositiveIntegerField()
    completion_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds")
    
    def __str__(self):
        return f"{self.user.username} - {self.drill_checklist.title} - {self.completion_percentage}%"
    
    class Meta:
        ordering = ['-completed_at']

class EmergencyContact(models.Model):
    """Model for emergency contacts"""
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    contact_type = models.CharField(max_length=50, choices=[
        ('fire', 'Fire Department'),
        ('police', 'Police'),
        ('medical', 'Medical Emergency'),
        ('disaster', 'Disaster Management'),
        ('school', 'School Administration'),
        ('local', 'Local Authority')
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.organization}"
    
    class Meta:
        ordering = ['contact_type', 'name']
