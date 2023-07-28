from django.db import models
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=70)
    slugname = models.CharField(max_length=70, default="")
    description = models.TextField()
    achieved_goals = models.TextField()
    used_technologies = models.TextField()
    photo = models.ImageField(upload_to="photos/%m")
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    global_priory = models.IntegerField()
    group_priory = models.IntegerField()
    is_published = models.BooleanField()
    source = models.URLField(default="")

    def get_achieved_goals_lst(self):
        return str(self.achieved_goals).split(", ")

    def get_used_technologies_lst(self):
        return str(self.used_technologies).split(", ")

    def save(self, *args, **kwargs):
        if not self.slugname:
            self.slugname = "_".join(str(self.title).lower().split())
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", kwargs={"type": self.category.slugname}) + f"#{self.slugname}"

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "Pet project"
        ordering = ["global_priory"]


class Category(models.Model):
    title = models.CharField(max_length=70)
    slugname = models.CharField(max_length=70, default="")
    description = models.TextField()
    photo = models.ImageField(upload_to="photos/%m")

    def save(self, *args, **kwargs):
        if not self.slugname:
            self.slugname = "_".join(str(self.title).lower().split())
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", kwargs={"type": self.slugname})

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "category of project"


class StudySource(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    knowledge = models.TextField()
    photo = models.ImageField(upload_to="photos/%m")
    source = models.URLField()
    order = models.IntegerField()

    def get_knowledge_lst(self):
        return str(self.knowledge).split(", ")

    def __str__(self):
        return self.title

    def get_ziped_description(self):

        def split_paragraph(p):
            ziped_p = ""
            symbols_per_row = 110
            start = 0
            i = symbols_per_row
            while i < len(p):
                j = i
                while p[j] != " ":
                    j -= 1
                ziped_p = ziped_p + p[start:j] + "\n"
                i = j + symbols_per_row
                start = j + 1
            ziped_p += p[start:]
            return ziped_p

        cur_desc = str(self.description)
        return "\n".join(list(map(split_paragraph, cur_desc.split("\n"))))

    class Meta():
        verbose_name = "Study source"


class Visit(models.Model):
    visiter_type = models.CharField(max_length=70)
    date = models.DateTimeField(auto_now_add=True)


def fill_db(previously_clear=True):
    if previously_clear:
        Project.objects.all().delete()
        Category.objects.all().delete()
        StudySource.objects.all().delete()


    stat_research = Category.objects.create(title="Statistical researches", description="description of statistical researches")
    kaggle_competitions = Category.objects.create(title="Kaggle competitions", description="description of kaggle competitions")
    programming = Category.objects.create(title="Programming", description="description of programming experience")

    work_analysis = Project.objects.create(title="Work analysis", description="Answers on all questions",
                                           category=stat_research, global_priory=1, group_priory=1)
    users_outflow = Project.objects.create(title="Users outflow", description="detecting patterns of behavior",
                                           category=stat_research, global_priory=2, group_priory=2)
    scrabble_rating_prediction = Project.objects.create(title="Scrabble rating prediction", description="Forecasting game's result before it's start",
                                                        category=kaggle_competitions, global_priory=3, group_priory=1)

    stat_course = StudySource.objects.create(title="Statistik", description="Entering into statistic",
                                             order=1, knowledge="statistic, A/B tests, bootstrap, mannu-uitny")
    ml_course = StudySource.objects.create(title="ML", description="Entering into ML",
                                             order=1, knowledge="ML, Gradient boosting")
