"""Модуль с объектами для OpenAPI (Swagger) документации.

Contains:
    ResponsesDict: Тип данных для обозначения словаря, описывающего ответы.
    JSONLikeDict: Тип данных JSON-подобных словарей.

Models:
    FieldDocsParams: Параметры документирования поля модели или параметра
        эндпоинта.
    EndpointDocsParams: Параметры документирования эндпоинта.
    ResponseDocsParams: Параметры документирования ответа.
    HeaderDocsParams: Параметры документирования заголовка.
    RouterDocsParams: Параметры документирования роутера.
"""

from typing import Any

from pydantic import BaseModel


ResponsesDict = dict[int | str, dict[str, Any]]
JSONLikeDict = dict[str, dict[str, Any]]


class _AbstractDocsParams(BaseModel):
    """Абстрактная модель параметров документирования.

    Значение None параметра означает отсутствие документации по этому
    параметру.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    def docs_dump(self) -> dict[str, Any]:
        """Дамп параметров документации в виде словаря.

        Исключает параметры, имеющие значения None. По сути представляет собой
        model_dump с exclude_none=True.

        Returns:
            dict[str, Any]: Словарь параметров документации.
        """
        return self.model_dump(exclude_none=True)


class FieldDocsParams(_AbstractDocsParams):
    """Параметры документирования поля модели или параметра эндпоинта.

    Значение None параметра означает отсутствие документации по этому
    параметру.

    Params:
        title (str | None): Имя поля. По умолчанию None.
        description (str | None): Описание поля. По умолчанию None.
        examples (list | None): Примеры значений поля. По умолчанию None.
        openapi_examples (list | None): Примеры значений поля в OpenAPI
            стилистике. По умолчанию None.
        deprecated (bool | None): Флаг устаревшести. По умолчанию None.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    title: str | None = None
    description: str | None = None
    examples: list | None = None
    openapi_examples: list | None = None
    deprecated: bool | None = None


class EndpointDocsParams(_AbstractDocsParams):
    """Параметры документирования эндпоинта.

    Значение None параметра означает отсутствие документации по этому
    параметру.

    Params:
        status_code (int | None): Статус-код обычного ответа. По умолчанию
            None.
        tags (list[str] | None): Список тегов. По умолчанию None.
        summary (str | None): Краткое описание. По умолчанию None.
        description (str | None): Описание. По умолчанию None.
        response_description (str | None): Описание обычного ответа. По
            умолчанию None
        responses (ResponsesDict | None): Ответы. По умолчанию None.
        deprecated (bool | None): Флаг устаревшести. По умолчанию None.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    status_code: int | None = None
    tags: list[str] | None = None
    summary: str | None = None
    description: str | None = None
    response_description: str | None = None
    responses: ResponsesDict | None = None
    deprecated: bool | None = None


class ResponseDocsParams(_AbstractDocsParams):
    """Параметры документирования ответа.

    Значение None параметра означает отсутствие документации по этому
    параметру.

    Params:
        model (BaseModel | None): Модель ответа. По умолчанию None.
        description (str | None): Описание. По умолчанию None.
        headers (JSONLikeDict | None): Заголовки. По умолчанию None.
        content (JSONLikeDict | None): Характеристика содержимого ответа. По
            умолчанию None.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    model: BaseModel | None = None
    description: str | None = None
    headers: JSONLikeDict | None = None
    content: JSONLikeDict | None = None


class HeaderDocsParams(_AbstractDocsParams):
    """Параметры документирования заголовка.

    Значение None параметра означает отсутствие документации по этому
    параметру.

    Params:
        description (str | None): Описание. По умолчанию None.
        schema_ (dict[str, str] | None): Схема заголовка для документирования.
            По умолчанию None. Является переименованием параметра schema
            документирования заголовков во избежание коллизии с одноименным
            параметром Pydantic-модели. При дампе имя меняется на нужное.
        required (bool | None): Флаг необходимости. По умолчанию None.
        deprecated (bool | None): Флаг устаревшести. По умолчанию None.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    description: str | None = None
    schema_: dict[str, str] | None = None
    required: bool | None = None
    deprecated: bool | None = None

    def docs_dump(self) -> dict[str, Any]:
        """Дамп параметров документации в виде словаря.

        Заменяет параметр schema_ на schema. Исключает параметры, имеющие
        значения None. По сути представляет собой model_dump с
        exclude_none=True.

        Returns:
            dict[str, Any]: Словарь параметров документации.
        """
        dump = self.model_dump(exclude_none=True)
        dump['schema'] = dump['schema_']
        del dump['schema_']
        return dump


class RouterDocsParams(_AbstractDocsParams):
    """Параметры документирования роутера.

    Значение None параметра означает отсутствие документации по этому
    параметру.

    Params:
        tags (list[str] | None): Список тегов. По умолчанию None.
        responses (ResponsesDict | None): Ответы. По умолчанию None.
    
    Methods:
        docs_dump: Дамп параметров документации.
    """

    tags: list[str] | None = None
    responses: ResponsesDict | None = None
