import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class Query(graphene.ObjectType):
    quiz = graphene.String()
    all_quizzes = DjangoListField(QuizzesType)
    single_quiz = graphene.Field(QuizzesType, id=graphene.Int())
    all_questions = DjangoListField(QuestionType)
    single_question = graphene.Field(QuestionType, id=graphene.Int())
    all_answers_for_question = graphene.List(AnswerType, id=graphene.Int())

    def resolve_quiz(root, info):
        return f'This is the first question'

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()
        # return Quizzes.objects.filter(id=1)

    def resolve_single_quiz(root, info, id):
        return Quizzes.objects.get(pk=id)

    def resolve_all_questions(root, info):
        return Question.objects.all()

    def resolve_single_question(root, info, id):
        return Question.objects.all(pk=id)

    def resolve_all_answers_for_question(root, info, id):
        return Answer.objects.filter(question=id)


class CategoryCreation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryCreation(category=category)


class CategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutation(category=category)


class Mutation(graphene.ObjectType):
    create_category = CategoryCreation.Field()
    update_category = CategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
