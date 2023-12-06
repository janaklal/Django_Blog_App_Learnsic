from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username = "testuser",
            email = "test@abc.com",
            password="testPass",
        )

        cls.post = Post.objects.create(
            title = "TestTitle",
            body="TestBody",
            author = cls.user,
        )
    def test_post_model(self):
        self.assertEqual(self.post.title,"TestTitle")
        self.assertEqual(self.post.body,"TestBody")
        self.assertEqual(self.post.author.username,"testuser")
        self.assertEqual(str(self.post),"TestTitle")
        self.assertEqual(self.post.get_absolute_url(),"/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code,200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"TestBody")
        self.assertTemplateUsed(response,"home.html")


    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail",
                                           kwargs={'pk':self.post.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"TestTitle")
        self.assertTemplateUsed(response,"post_detail.html")

    def test_post_detailview_no_response(self):
        no_response = self.client.get("/post/99999/")
        self.assertEqual(no_response.status_code,404)

    
    def test_post_create(self):
        response = self.client.post(reverse("post_new"),
                                    {
                                     "title":"New Title",
                                     "body":"New Body",
                                     "author":self.user.id,   
                                    })
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"New Title")
        self.assertEqual(Post.objects.last().body,"New Body")


    def test_post_update(self):
        response = self.client.post(reverse("post_edit",args="1"),
                                    {
                                        "title":"Updated Title",
                                        "body":"Updated Body",
                                    })
        self.assertAlmostEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"Updated Title")
        self.assertEqual(Post.objects.last().body,"Updated Body")



