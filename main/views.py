from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import json
from datetime import datetime, timedelta

from .models import (
    DisasterType, EducationModule, Quiz, QuizQuestion, DrillChecklist,
    UserProfile, ModuleProgress, QuizAttempt, DrillCompletion, EmergencyContact
)

def home(request):
    """Home page with overview of disaster types"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    disaster_types = DisasterType.objects.all()
    total_modules = EducationModule.objects.count()
    total_quizzes = Quiz.objects.count()
    
    context = {
        'disaster_types': disaster_types,
        'total_modules': total_modules,
        'total_quizzes': total_quizzes,
    }
    return render(request, 'home.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            user_type = request.POST.get('user_type', 'student')
            institution = request.POST.get('institution', '')
            grade_level = request.POST.get('grade_level', '')
            
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                institution=institution,
                grade_level=grade_level
            )
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard showing progress and available content"""
    disaster_types = DisasterType.objects.all()
    user_progress = {}
    
    for disaster_type in disaster_types:
        modules = disaster_type.modules.all()
        completed_modules = ModuleProgress.objects.filter(
            user=request.user,
            module__disaster_type=disaster_type,
            completed=True
        ).count()
        
        quiz_attempts = QuizAttempt.objects.filter(
            user=request.user,
            quiz__disaster_type=disaster_type
        )
        
        drill_completions = DrillCompletion.objects.filter(
            user=request.user,
            drill_checklist__disaster_type=disaster_type
        )
        
        user_progress[disaster_type.id] = {
            'modules_completed': completed_modules,
            'total_modules': modules.count(),
            'quiz_attempts': quiz_attempts.count(),
            'avg_quiz_score': quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0,
            'drill_completions': drill_completions.count(),
            'avg_drill_score': drill_completions.aggregate(Avg('completion_percentage'))['completion_percentage__avg'] or 0,
        }
    
    # Recent activity
    recent_modules = ModuleProgress.objects.filter(
        user=request.user,
        completed=True
    ).order_by('-completion_date')[:5]
    
    recent_quizzes = QuizAttempt.objects.filter(
        user=request.user
    ).order_by('-completed_at')[:5]
    
    context = {
        'disaster_types': disaster_types,
        'user_progress': user_progress,
        'recent_modules': recent_modules,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'dashboard.html', context)

@login_required
def module_detail(request, module_id):
    """Display education module content"""
    module = get_object_or_404(EducationModule, id=module_id)
    
    # Check if user has completed this module
    progress, created = ModuleProgress.objects.get_or_create(
        user=request.user,
        module=module,
        defaults={'time_spent': 0}
    )
    
    # Get other modules in the same disaster type
    related_modules = EducationModule.objects.filter(
        disaster_type=module.disaster_type
    ).exclude(id=module_id).order_by('order')
    
    # Get available quiz for this disaster type
    quiz = Quiz.objects.filter(disaster_type=module.disaster_type).first()
    
    context = {
        'module': module,
        'progress': progress,
        'related_modules': related_modules,
        'quiz': quiz,
    }
    return render(request, 'module_detail.html', context)

@login_required
@require_POST
def complete_module(request, module_id):
    """Mark a module as completed"""
    module = get_object_or_404(EducationModule, id=module_id)
    
    progress, created = ModuleProgress.objects.get_or_create(
        user=request.user,
        module=module
    )
    
    if not progress.completed:
        progress.completed = True
        progress.completion_date = timezone.now()
        
        # Add time spent (from frontend)
        time_spent = request.POST.get('time_spent', 0)
        try:
            progress.time_spent = int(time_spent)
        except (ValueError, TypeError):
            progress.time_spent = 0
        
        progress.save()
        messages.success(request, f'Module "{module.title}" completed!')
    
    return redirect('module_detail', module_id=module_id)

@login_required
def quiz_detail(request, quiz_id):
    """Display quiz questions"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().order_by('order')
    
    # Check previous attempts
    previous_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz
    ).order_by('-completed_at')
    
    best_score = previous_attempts.aggregate(
        best=models.Max('score')
    )['best'] or 0
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'previous_attempts': previous_attempts[:5],  # Show last 5 attempts
        'best_score': best_score,
    }
    return render(request, 'quiz.html', context)

@login_required
@require_POST
def submit_quiz(request, quiz_id):
    """Process quiz submission"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    correct_answers = 0
    total_questions = questions.count()
    
    # Calculate score
    for question in questions:
        user_answer = request.POST.get(f'question_{question.id}')
        if user_answer and user_answer.upper() == question.correct_answer:
            correct_answers += 1
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Get time taken
    time_taken = request.POST.get('time_taken', 0)
    try:
        time_taken = int(time_taken)
    except (ValueError, TypeError):
        time_taken = 0
    
    # Save quiz attempt
    QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        time_taken=time_taken
    )
    
    messages.success(request, f'Quiz completed! Score: {score:.1f}% ({correct_answers}/{total_questions})')
    return redirect('quiz_detail', quiz_id=quiz_id)

@login_required
def drill_checklist(request, drill_id):
    """Display drill checklist"""
    drill = get_object_or_404(DrillChecklist, id=drill_id)
    steps = drill.steps.all().order_by('order')
    
    # Get previous completions
    previous_completions = DrillCompletion.objects.filter(
        user=request.user,
        drill_checklist=drill
    ).order_by('-completed_at')
    
    best_completion = previous_completions.aggregate(
        best=models.Max('completion_percentage')
    )['best'] or 0
    
    context = {
        'drill': drill,
        'steps': steps,
        'previous_completions': previous_completions[:5],
        'best_completion': best_completion,
    }
    return render(request, 'drill_checklist.html', context)

@login_required
@require_POST
def complete_drill(request, drill_id):
    """Process drill completion"""
    drill = get_object_or_404(DrillChecklist, id=drill_id)
    total_steps = drill.steps.count()
    
    # Count completed steps
    completed_steps = 0
    for step in drill.steps.all():
        if request.POST.get(f'step_{step.id}') == 'on':
            completed_steps += 1
    
    completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    # Get time taken
    time_taken = request.POST.get('time_taken', 0)
    try:
        time_taken = int(time_taken)
    except (ValueError, TypeError):
        time_taken = 0
    
    # Save drill completion
    DrillCompletion.objects.create(
        user=request.user,
        drill_checklist=drill,
        completed_steps=completed_steps,
        total_steps=total_steps,
        completion_percentage=completion_percentage,
        time_taken=time_taken
    )
    
    messages.success(request, f'Drill completed! {completion_percentage:.1f}% ({completed_steps}/{total_steps} steps)')
    return redirect('drill_checklist', drill_id=drill_id)

@login_required
def emergency_contacts(request):
    """Display emergency contacts"""
    contacts = EmergencyContact.objects.filter(is_active=True).order_by('contact_type', 'name')
    
    # Group contacts by type
    grouped_contacts = {}
    for contact in contacts:
        contact_type = contact.get_contact_type_display()
        if contact_type not in grouped_contacts:
            grouped_contacts[contact_type] = []
        grouped_contacts[contact_type].append(contact)
    
    context = {
        'grouped_contacts': grouped_contacts,
    }
    return render(request, 'emergency_contacts.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard for teachers and administrators"""
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile or user_profile.user_type not in ['teacher', 'admin']:
        messages.error(request, 'Access denied. Teacher or Administrator privileges required.')
        return redirect('dashboard')
    
    # Get statistics
    total_users = UserProfile.objects.count()
    student_count = UserProfile.objects.filter(user_type='student').count()
    teacher_count = UserProfile.objects.filter(user_type='teacher').count()
    
    # Recent activity
    recent_module_completions = ModuleProgress.objects.filter(
        completed=True
    ).order_by('-completion_date')[:10]
    
    recent_quiz_attempts = QuizAttempt.objects.order_by('-completed_at')[:10]
    
    # Progress by disaster type
    disaster_progress = []
    for disaster_type in DisasterType.objects.all():
        modules = disaster_type.modules.all()
        total_modules = modules.count()
        
        completed_count = ModuleProgress.objects.filter(
            module__disaster_type=disaster_type,
            completed=True
        ).count()
        
        avg_quiz_score = QuizAttempt.objects.filter(
            quiz__disaster_type=disaster_type
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        disaster_progress.append({
            'disaster_type': disaster_type,
            'completion_rate': (completed_count / (total_modules * student_count * 100)) if total_modules > 0 and student_count > 0 else 0,
            'avg_quiz_score': avg_quiz_score,
        })
    
    context = {
        'total_users': total_users,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'recent_module_completions': recent_module_completions,
        'recent_quiz_attempts': recent_quiz_attempts,
        'disaster_progress': disaster_progress,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def get_progress(request, disaster_id):
    """API endpoint to get user progress for a specific disaster type"""
    disaster_type = get_object_or_404(DisasterType, id=disaster_id)
    
    modules = disaster_type.modules.all()
    completed_modules = ModuleProgress.objects.filter(
        user=request.user,
        module__disaster_type=disaster_type,
        completed=True
    )
    
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz__disaster_type=disaster_type
    )
    
    data = {
        'disaster_type': disaster_type.name,
        'modules_completed': completed_modules.count(),
        'total_modules': modules.count(),
        'completion_rate': (completed_modules.count() / modules.count() * 100) if modules.count() > 0 else 0,
        'quiz_attempts': quiz_attempts.count(),
        'best_quiz_score': quiz_attempts.aggregate(models.Max('score'))['score__max'] or 0,
        'avg_quiz_score': quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0,
    }
    
    return JsonResponse(data)
