# from django.db import models
# from apps.users.models import User

# class ImageAlbum(models.Model):
#     path = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, related_name="albums", on_delete=models.CASCADE)
    
#     def __str__(self) -> str:
#         return self.path

#     def default(self):
#         return self.images.filter(default=True).first()

# def get_upload_path(instance, filename):
#     return f'{instance.album.path}/{filename}'

# class Image(models.Model):
#     base = models.ImageField(upload_to=get_upload_path)
#     album = models.ForeignKey(ImageAlbum, related_name="images", on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     default = models.BooleanField(null=True, default=None, blank=True)