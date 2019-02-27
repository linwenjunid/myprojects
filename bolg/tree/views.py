from django.shortcuts import render_to_response, render
from .models import Comments
from xadmin.views import BaseAdminView


class CommentsView(BaseAdminView):
    def get(self, request, *args, **kwargs):
        comments = Comments.objects.all()
        return render_to_response('tree/comments.html', {'comments': comments})
        #return render(request, template_name, context)
