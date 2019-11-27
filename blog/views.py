from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category, Post, Media
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
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
            media = get_object_or_404(Media, id=data["media"])
            data["media"] = media
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
        return JsonResponse({"success": "true"}, status=204)

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


@csrf_exempt
def categorise(request):
    if request.method == "POST":
        data = request.data
        cate = Category.objects.create(**data)
        return JsonResponse(cate, status=201)
    if request.method == "GET":
        cates = list(Category.objects.values())
        return JsonResponse(cates, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def category(request, slug):
    if request.method == 'PATCH':
        data = request.data
        cate = get_object_or_404(Category, slug=slug)
        for key, value in data.items():
            setattr(cate, key, value)
        cate.save(update_fields=list(data.keys()))
        return JsonResponse(cate, status=201)
    if request.method == "DELETE":
        data = request.data
        cate = get_object_or_404(Category, slug=slug)
        cate.delete()
        return JsonResponse(status=204)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def media(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        alter = request.POST.get('alter')
        name = request.POST.get('name')
        if not image:
            return JsonResponse({"error": "you have to upload a photo"}, status=403)
        media = Media.objects.create(pic=image, name=name, pic_alter=alter)
        return JsonResponse({"id": media.id, "name": media.name}, status=201)
    return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
def edit_media(request, id):
    if request.method == "PUT":
        image = request.form.get('image')
        alter = request.form.get('alter')
        name = request.form.get('name')
        if not all([image,alter,name]):
            return JsonResponse({"error": "You have to enter every 3 fields.(name, alter, image)"}, status=400)
        media = Media.objects.filter(id=id).update(pic=image, name=name, pic_alter=alter)
        if media == 0:
            return JsonResponse({"error": "the media didn't exist."}, status=400)
        return JsonResponse({"success": "media updated success fully"})
    return JsonResponse({"error": "Method not allowed"}, status=405)
        
