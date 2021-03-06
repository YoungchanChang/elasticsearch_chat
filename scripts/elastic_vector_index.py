from app.infrastructure.database.elastic_conn import *
from app.config.settings import *


def set_wiki_index(elastic_index: str):

    result = es.indices.delete(index=elastic_index, ignore=[400, 404])
    print(result)

    body = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "nori_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                            ]
                        },
                        "nori_noun_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                                "part_of_speech_noun",
                            ]
                        },
                        "nori_verb_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                                "part_of_speech_verb",
                            ]
                        }
                    },
                    "tokenizer": {
                        "wiki_dict_tokenizer": {
                            "type": "nori_tokenizer",
                        },
                    },
                    # 동의어 추가 및 제거할 단어
                    "filter": {
                        "part_of_speech_noun": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                                "NP", "NNB", # 대명사, 의존명사
                                "SF", # 마침표
                                "E", "J", "IC", "MAG", "MAJ", "NA", "SC",
                                "SE", "SH", "SP", "SSC", "SSO", "UNA",
                                "VCP", "VCN", "VSV", "XPN", "XSA", "XSV", "SY", "VA", "VV", "VX"
                            ]
                        },
                        "part_of_speech_verb": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                                "NNG", "NNP", "NNB", "NNBC", "NR", "NP",
                                "VX", "VCP", "VCN",
                                "MAG", "MAJ", "MM",
                                "IC",
                                "J",
                                "E",
                                "VX", "VCP", "VCN",
                                "SP", "SSC", "SSO", "SC", "SE", "SH", "SN",
                                "XPN", "XSA", "XSN", "XSV",
                                "UNA", "NA", "VSV"
                            ]
                        }

                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content_vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine"
                },
                "title": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },
                },
                "first_header": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },
                },
                "second_header": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },

                },
                "content": {
                    "type": "text",
                    "analyzer": "nori_noun_analyzer",
                    "fielddata": True
                },
                "content_noun_search": {
                    "type": "keyword"
                },
                "content_verb_search": {
                    "type": "keyword"
                }
            }
        }
    }

    ans = es.indices.create(index=elastic_index, body=body, ignore=400, )
    print(ans)


def exists_index():
    es_alias = es.indices.get_alias().keys()
    if "wiki-vector-index" not in es_alias:
        set_wiki_index()

if __name__ == '__main__':

    set_wiki_index(elastic_vector_index)

