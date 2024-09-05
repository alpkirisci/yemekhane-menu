from django.http import HttpResponse
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView


class BaseFormSetView(ModelFormMixin, ProcessFormView):
    formset_class = None  # Formset class to be used.
    # Field on the model related to the formset.
    formset_related_field = None

    # Will be built with get or post.
    formset = None

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_formset_queryset(self):
        """Return queryset for building initial form with GET."""
        # If there is an associated object use it.
        if self.object is not None:
            related_field = self.formset_related_field
            if related_field is None:
                raise ValueError("You must define 'formset_related_field' in the view.")
            return getattr(self.object, related_field).all()
        else:
            return self.model.objects.none()

    def get_context_data(self, **kwargs):
        """Add formset to context."""
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        """Build formset with POST request"""
        if self.formset_class is None:
            raise ValueError("You must define 'formset_class' in the view.")
        # Construct formset
        self.formset = self.formset_class(request.POST)
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Build formset with GET request"""
        if self.formset_class is None:
            raise ValueError("You must define 'formset_class' in the view.")
        # Construct formset
        self.formset = self.formset_class(queryset=self.get_formset_queryset())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Handle formset validation and response with HX-Redirect."""
        if self.formset.is_valid():
            # TODO: Seperate HX-Redirect related lines from class
            # Save the form and get response.
            response = super().form_valid(form)
            # Dumb it down to get rid of Location header.
            response = HttpResponse(response)
            # Modify response to add HX-Redirect.
            response['HX-Redirect'] = self.get_success_url()

            related_field = self.formset_related_field
            if related_field is None:
                raise ValueError("You must define 'formset_related_field' in the view.")

            # Save formset items.
            items = self.formset.save()
            # Add items to instance.related_field.
            getattr(form.instance, related_field).add(*items)

            return response
        else:
            return self.form_invalid(form)


class FormSetUpdateView(SingleObjectTemplateResponseMixin, BaseFormSetView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class FormSetCreateView(SingleObjectTemplateResponseMixin, BaseFormSetView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)
