from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category, Post
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, get_object_or_404
import json


@method_decorator(csrf_exempt, name='dispatch')
class PostsView(View):
    data = {}
    def get(self, request):
        posts = list(Post.objects.values())
        return JsonResponse(posts, safe=False)

    def post(self, request):
        data = self.data
        if data.get("category"):
            category = get_object_or_404(Category, id=data["category"])
            data["category"] = category
        if data.get("media"):
            category = get_object_or_404(Category, id=data["media"])
            data["media"] = category
        try:
            post = Post.objects.create(**data)
        except IntegrityError:
            return JsonResponse({"error": "The slug could not be repetitive"}, status=403)
        data["id"] = post.id
        data["pub_date"] = post.pub_date
        return JsonResponse(data, status=201)

    def setup(self, request, *args, **kwargs):
        if request.method != "GET":
            data = json.loads(request.body)
            category = data.get("category")
            media = data.get("media")
            int_validate = [category, media]
            for i in int_validate:
                if i and not isinstance(i, int):
                    raise PermissionDenied
            self.data = data
        return super(PostsView, self).setup(request, *args, **kwargs)



@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):
    data = {}
    def get(self, request, slug=None):
        post = Post.objects.filter(slug=slug).values()
        if bool(post):
            post = post[0]
            return JsonResponse(post)
        return JsonResponse({"success": "false"}, status=404)
    
    def patch(self, request, slug=None):
        data = self.data
        blog = get_object_or_404(Post, slug=slug)
        if data.get("category"):
            data["catgory"] = get_object_or_404(Category, id=data["category"])
        if data.get("media"):
            data["media"] = get_object_or_404(Category, id=data["media"])
        for key, value in data.items():
            setattr(blog, key, value)
        blog.save(update_fields=list(data.keys()))
        return JsonResponse({"patch": slug})

    def put(self, request, slug=None):
        data = self.data
        blog = get_object_or_404(Post, slug=slug)
        if data.get("category"):
            data["catgory"] = get_object_or_404(Category, id=data["category"])
        if data.get("media"):
            data["media"] = get_object_or_404(Category, id=data["media"])
        for key, value in data.items():
            setattr(blog, key, value) 
        blog.save() 
        data["id"] = blog.id
        data["pub_date"] = blog.pub_date   
        return JsonResponse(data, status=202)

    def delete(self, request, slug=None):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return JsonResponse({"success":"true"}, status=204)

    def setup(self, request, *args, **kwargs):
        if request.method != "GET":
            data = json.loads(request.body)
            category = data.get("category")
            media = data.get("media")
            int_validate = [category, media]
            for i in int_validate:
                if i and not isinstance(i, int):
                    raise PermissionDenied
            self.data = data
        return super(PostView, self).setup(request, *args, **kwargs)
    



