from pydantic import BaseModel
from typing import List, Optional

class VerseResult(BaseModel):
    id: int
    score: float
    quran_id: int
    surah_id: int
    ayah_id: int
    juz_id: int
    surah_type: str
    arabic_text: str
    english_text: str
    urdu_text: str
    surah_name_ar: Optional[str] = ""
    surah_name_ur: Optional[str] = ""
    surah_name_en: Optional[str] = ""
    transliteration: Optional[str] = ""

class LLMExplanation(BaseModel):
    urdu: str
    verses_used: List[int]

class SearchResponse(BaseModel):
    query: str
    processed_query: str
    top_results: List[VerseResult]
    llm_explanation: LLMExplanation

class Query(BaseModel):
    text: str
    top_k: int = 5