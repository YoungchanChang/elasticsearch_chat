import json
import requests
from requests.auth import HTTPBasicAuth
from elasticsearch import helpers


from app.application.repo_interface import AbstractRepository, AbstractFinder
import app.controller.mrc_controller as mrc_con
from app.domain.custome_error import WikiDataException
from app.domain.domain import WikiQuestionItemDTO
from app.infrastructure.database.elastic_conn import es
from app.config.settings import *

json_header = {'Content-Type':'application/json'}


class ElasticContent(AbstractRepository):

    def create(self, model: WikiQuestionItemDTO):

        """
        위키피디아에서 검색 후 데이터 생성
        :param model: 위키피디아 주제, 질문 데이터
        :return:
        """
        wiki_control = mrc_con.WikiControl()
        result = helpers.bulk(es, wiki_control.gen_vector_data(model.title))
        return result

    def find_one(self, model: WikiQuestionItemDTO):

        result = es.search(index=elastic_vector_index, body=mrc_con.get_encoded_content_template(model.title, model.question))
        resp = result.body
        return resp['hits']['hits']


class ElasticTitle(AbstractFinder):

    def find_one(self, model: WikiQuestionItemDTO):
        result = es.search(index=elastic_vector_index, body=mrc_con.get_encoded_title_template(model.question))
        resp = result.body
        return resp['hits']['hits'][0]["_source"]['title']

