import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import POSTGRES_CONFIG
from services.logger import logger
from typing import List, Dict, Any

def get_verse_texts_from_db(verse_details: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fetch verse texts from PostgreSQL using quran_id
    """
    if not verse_details:
        logger.warning("No verse details provided")
        return []
    
    # Extract quran_ids
    quran_ids = [detail["quran_id"] for detail in verse_details if detail.get("quran_id")]
    
    if not quran_ids:
        logger.warning("No valid quran_ids found")
        return []
    
    logger.info(f"Fetching {len(quran_ids)} verses from PostgreSQL")
    
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        SELECT 
            quran_id,
            juz_id,
            surah_id,
            ayah_id,
            source,
            transliteration,
            surah_name_ar,
            surah_name_ur,
            surah_name_en,
            surah_type,
            text_ar,
            text_ur,
            text_en
        FROM quran_ayah 
        WHERE quran_id = ANY(%s)
        ORDER BY array_position(%s, quran_id)
        """
        
        cursor.execute(query, (quran_ids, quran_ids))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Retrieved {len(results)} verses from PostgreSQL")
        
        # Convert to list of dicts
        verse_texts = []
        for row in results:
            verse_texts.append(dict(row))
        
        return verse_texts
        
    except Exception as e:
        logger.error(f"PostgreSQL error: {str(e)}")
        
        # Fallback data
        fallback_data = []
        for quran_id in quran_ids:
            fallback_data.append({
                "quran_id": quran_id,
                "text_ar": f"آية {quran_id}",
                "text_en": f"Verse {quran_id}",
                "text_ur": f"آیت {quran_id}",
                "surah_name_ar": "",
                "surah_name_ur": "",
                "surah_name_en": "",
                "transliteration": ""
            })
        
        return fallback_data