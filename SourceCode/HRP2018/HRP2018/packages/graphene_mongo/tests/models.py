from datetime import datetime
from mongoengine import (
    connect, Document, EmbeddedDocument
)
from mongoengine.fields import (
    DateTimeField, EmailField, EmbeddedDocumentField,
    FloatField, EmbeddedDocumentListField, ListField,
    MapField, ReferenceField, StringField
)

connect('graphene-mongo-test', host='mongomock://localhost', alias='default')


class Editor(Document):

    meta = {'collection': 'test_editor'}
    id = StringField(primary_key=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    metadata = MapField(field=StringField())


class Pet(Document):

    meta = {'collection': 'test_pet'}
    name = StringField(max_length=16, required=True)
    reporter_id = StringField()


class Article(Document):

    meta = {'collection': 'test_article'}
    headline = StringField(required=True)
    pub_date = DateTimeField(default=datetime.now)
    editor = ReferenceField(Editor)
    reporter = ReferenceField('Reporter')


class EmbeddedArticle(EmbeddedDocument):

    meta = {'collection': 'test_embedded_article'}
    headline = StringField(required=True)
    pub_date = DateTimeField(default=datetime.now)
    editor = ReferenceField(Editor)
    reporter = ReferenceField('Reporter')


class Reporter(Document):

    meta = {'collection': 'test_repoter'}
    id = StringField(primary_key=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField()
    articles = ListField(ReferenceField(Article))
    embedded_articles = ListField(EmbeddedDocumentField(EmbeddedArticle))
    embedded_list_articles = EmbeddedDocumentListField(EmbeddedArticle)
    awards = ListField(StringField())


class Player(Document):

    meta = {'collection': 'test_player'}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    opponent = ReferenceField('Player')
    players = ListField(ReferenceField('Player'))
    articles = ListField(ReferenceField('Article'))
    embedded_list_articles = EmbeddedDocumentListField(EmbeddedArticle)


class Parent(Document):

    meta = {
        'collection': 'test_parent',
        'allow_inheritance': True
    }
    bar = StringField()


class Child(Parent):

    meta = {'collection': 'test_child'}
    baz = StringField()


class ProfessorMetadata(EmbeddedDocument):

    meta = {'collection': 'test_professor_metadata'}
    id = StringField(primary_key=False)
    first_name = StringField()
    last_name = StringField()
    departments = ListField(StringField())


class ProfessorVector(Document):

    meta = {'collection': 'test_professor_vector'}
    vec = ListField(FloatField())
    metadata = EmbeddedDocumentField(ProfessorMetadata)
