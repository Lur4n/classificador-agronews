# models.py
from typing import List, Optional
from pydantic import BaseModel, Field


class CategoriaInference(BaseModel):
    nome: str = Field(
        ..., description="Nome exato da categoria (ex: 'Grãos', 'Pecuária', 'Economia')"
    )
    percentual: float = Field(
        ..., ge=0.0, le=100.0, description="Percentual de relevância (0 a 100)"
    )


class ClassificacaoResultado(BaseModel):
    categoria_principal: str = Field(
        ..., description="A categoria com maior percentual de probabilidade"
    )
    distribuicao: List[CategoriaInference] = Field(
        default_factory=list,
        description="Lista de categorias e seus respetivos percentuais"
    )
    resumo_curto: Optional[str] = Field(
        None, description="Resumo opcional gerado pelo modelo"
    )


class NoticiaInput(BaseModel):
    id: Optional[int] = None
    titulo: str
    conteudo: str