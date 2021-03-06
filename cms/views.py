from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from .models import Image


@login_required
def upload_image(request):
    f = request.FILES.get('editormd-image-file')
    img = Image(image=f)
    img.save()
    return JsonResponse({
        'success': 1,           # 0表示上传失败;1表示上传成功
        'message': "success",
        'url': img.image.url    # 上传成功时才返回
    })
