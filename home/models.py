from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User
from PIL import Image

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return str(self.category)

class Subcategory(models.Model):
    obj = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50, default=None, null=True)
    jobbycategory = models.CharField(max_length=200)
    jobdescription = models.TextField(null=True, blank=False)
    postdate =  models.DateField(default=date.today)

    def __str__(self):
        return str(self.obj)+'=>'+self.subcategory+'=>'+self.jobbycategory

class Admitcard(models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    admitcard = models.CharField(max_length=300)
    postdate =  models.DateField(default=date.today)
    def __str__(self):
        return str(self.job)+'=>'+str(self.admitcard)

class Result(models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    result = models.CharField(max_length=300)
    postdate =  models.DateField(default=date.today)
    def __str__(self):
        return str(self.job)+'=>'+str(self.result)

class Subjectcategory(models.Model):
    obj = models.ForeignKey(Category,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)

    def __str__(self):
        return str(self.obj)+' '+self.subject

class Quiz(models.Model):
    subject = models.ForeignKey(Subjectcategory,on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=50)
    quiz_time = models.IntegerField(default=60)
    quiz_created = models.DateField(default=date.today)
    total_question = models.IntegerField(default=10)
    def __str__(self):
        return str(self.subject)+'=>'+str(self.quiz_title)

class Quiz_question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question_no = models.IntegerField(default=1)
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    option5 = models.TextField(blank=True)
    user_answer = models.TextField(blank= True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    def __str__(self):
        return str(self.quiz)+' '+str(self.question_no)

class Prevpaper(models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    paper_title = models.CharField(max_length=50)
    paper_time = models.IntegerField(default=60)
    paper_year = models.IntegerField()
    total_question = models.IntegerField(default=100)
    def __str__(self):
        return str(self.paper_title)+'=>'+str(self.paper_year)

class Prev_question(models.Model):
    prev_paper = models.ForeignKey(Prevpaper,on_delete=models.CASCADE)
    question_no = models.IntegerField(default=1)
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    option5 = models.TextField(blank=True)
    user_answer = models.TextField(blank= True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    def __str__(self):
        return str(self.prev_paper)+' '+str(self.question_no)

class Tarik (models.Model):
    date = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    allheading = models.CharField(max_length=100,default='default')
    alldates = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return str(self.date)+'=>'+str(self.allheading)

class Appfees (models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    category = models.CharField(max_length=500,default='default')
    fees = models.DecimalField(default=0.00,decimal_places=2,max_digits=10000)
    def __str__(self):
        return str(self.job)+'=>'+str(self.category)

class Vacancyheader(models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    header = models.CharField(max_length=200)
    def __str__(self):
        return str(self.job)+'=>'+str(self.header)

class Vacancydetail (models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    gen = models.IntegerField(default=0)
    obc = models.IntegerField(default=0)
    sc = models.IntegerField(default=0)
    st = models.IntegerField(default=0)
    pwd = models.IntegerField(default=0,blank=True)
    gen_female = models.IntegerField(default=0,blank=True)
    obc_female = models.IntegerField(default=0,blank=True)
    sc_female = models.IntegerField(default=0,blank=True)
    st_female = models.IntegerField(default=0,blank=True)
    Total = models.IntegerField(default=0,blank=True)
    ex_serviceman = models.IntegerField(default=0,blank=True)
    eligibility = models.CharField(max_length=1000)
    def __str__(self):
        return self.department

class Links(models.Model):
    job = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    link_type = models.CharField(max_length=100)
    link = models.CharField(max_length=500)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)