import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Education,
    Experience,
    Skill,
    Project,
    ProfileLink,
    Certification
)
from .forms import (
    UserProfileForm,
    EducationForm,
    ExperienceForm,
    SkillForm,
    ProjectForm,
    ProfileLinkForm,
    CertificationForm
)

DEFAULT_USER = settings.DEFAULT_USER_ID


class HomeView(View):
    @staticmethod
    def has_section(qs):
        return qs.exists()

    def get(self, *args, **kwargs):
        user = str(self.request.user)
        profile_qs = None
        context = {}
        if self.request.GET.get('user_name'):
            try:
                user = User.objects.get(username=self.request.GET.get('user_name')).id
                profile_qs = UserProfile.objects.filter(user__id=user)[0]
            except ObjectDoesNotExist:
                messages.warning(self.request, "None Found With The Given Username")
                return redirect('portfolio_app:home')
        elif user == "AnonymousUser":
            user = DEFAULT_USER
            profile_qs = UserProfile.objects.filter(user__id=user)[0]
        else:
            user = self.request.user
            profile_qs = UserProfile.objects.filter(user__id=user.id)[0]
        education_qs = Education.objects.filter(user=user).order_by('degree')
        experience_qs = Experience.objects.filter(user=user)
        professional_project_qs = Project.objects.filter(user=user, project_type="P1")
        personal_project_qs = Project.objects.filter(user=user, project_type="P2")
        skill_qs = Skill.objects.filter(user=user)
        certification_qs = Certification.objects.filter(user=user)
        profile_link_qs = ProfileLink.objects.filter(user=user)
        context['has_education'] = self.has_section(education_qs)
        context['has_experience'] = self.has_section(experience_qs)
        context['has_professional_project'] = self.has_section(professional_project_qs)
        context['has_personal_project'] = self.has_section(personal_project_qs)
        context['has_certification'] = self.has_section(certification_qs)
        context['has_profile_link'] = self.has_section(profile_link_qs)
        context['has_skill'] = self.has_section(skill_qs)
        context['profile'] = profile_qs
        context['education'] = education_qs
        context['experience'] = experience_qs
        context['professional_project'] = professional_project_qs
        context['personal_project'] = personal_project_qs
        context['skill'] = skill_qs
        context['certification'] = certification_qs
        context['profile_link'] = profile_link_qs
        return render(self.request, 'index.html', context)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {}
        profile_qs = UserProfile.objects.filter(user=self.request.user)[0]
        education_qs = Education.objects.filter(user=self.request.user).order_by('degree')
        experience_qs = Experience.objects.filter(user=self.request.user)
        personal_project_qs = Project.objects.filter(user=self.request.user)
        skill_qs = Skill.objects.filter(user=self.request.user)
        certification_qs = Certification.objects.filter(user=self.request.user)
        profile_link_qs = ProfileLink.objects.filter(user=self.request.user)
        context['user_profile'] = profile_qs
        context['user_education'] = education_qs
        context['user_experience'] = experience_qs
        context['user_project'] = personal_project_qs
        context['user_skill'] = skill_qs
        context['user_certification'] = certification_qs
        context['user_profile_link'] = profile_link_qs
        return render(self.request, 'profile/user_profile.html', context)


class AddEducationView(LoginRequiredMixin, CreateView):
    model = Education
    template_name = 'education_form.html'
    form_class = EducationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddEducationView, self).form_valid(form)


class AddExperienceView(LoginRequiredMixin, CreateView):
    model = Experience
    template_name = 'experience_form.html'
    form_class = ExperienceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddExperienceView, self).form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class AddSkillView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        for d in data:
            Skill.objects.get_or_create(user=self.request.user, skill=str(d).capitalize())
        response = {
            "response": "ok"
        }
        messages.success(self.request, "Skills Updated Successfully")
        return JsonResponse(response, safe=False)

    def get(self, *args, **kwargs):
        data = Skill.objects.filter(user=self.request.user).order_by('-id')
        return render(self.request, 'skill_form.html', {"data": data, "host": self.request.get_host()})


class AddProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddProjectView, self).form_valid(form)


class AddProfileLinkView(LoginRequiredMixin, CreateView):
    model = ProfileLink
    template_name = 'profilelink_form.html'
    form_class = ProfileLinkForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddProfileLinkView, self).form_valid(form)


class AddCertificationView(LoginRequiredMixin, CreateView):
    model = Certification
    template_name = 'certification_form.html'
    form_class = CertificationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCertificationView, self).form_valid(form)


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'user_profile_form.html'
    form_class = UserProfileForm

    def form_valid(self, form):
        return super(UpdateUserProfileView, self).form_valid(form)


class UpdateEducationView(LoginRequiredMixin, UpdateView):
    model = Education
    template_name = 'education_form.html'
    form_class = EducationForm

    def form_valid(self, form):
        return super(UpdateEducationView, self).form_valid(form)


class UpdateExperienceView(LoginRequiredMixin, UpdateView):
    model = Experience
    template_name = 'experience_form.html'
    form_class = ExperienceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateExperienceView, self).form_valid(form)


class UpdateSkillView(LoginRequiredMixin, UpdateView):
    pass


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateProjectView, self).form_valid(form)


class UpdateProfileLinkView(LoginRequiredMixin, UpdateView):
    model = ProfileLink
    template_name = 'profilelink_form.html'
    form_class = ProfileLinkForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateProfileLinkView, self).form_valid(form)


class UpdateCertificationView(LoginRequiredMixin, UpdateView):
    model = Certification
    template_name = 'certification_form.html'
    form_class = CertificationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateCertificationView, self).form_valid(form)


class DeleteSkillView(DeleteView):
    model = Skill
    success_url = reverse_lazy('/portfolio/user_profile/')
    template_name = 'profile/delete_skill.html'


def delete_skill(request, pk):
    try:
        skill_to_delete = Skill.objects.get(pk=pk)
        skill_to_delete.delete()
        messages.success(request, "Successfully Deleted")
        return redirect('portfolio_app:profile')
    except ObjectDoesNotExist:
        messages.warning(request, "Opps!! The object does not exist")
        return redirect('portfolio_app:profile')


class SendEmailView(View):
    def post(self, *args, **kwargs):
        sender = self.request.POST['email']
        receiver = self.request.POST['user_email']
        subject = "Portfolio Email"
        message = self.request.POST['message'] + "\n" + f"from email {sender}"
        send_mail(
            subject,
            message,
            sender,
            [receiver],
            fail_silently=False
        )
        return JsonResponse({"message": "Email has been sent successfully!!"})

