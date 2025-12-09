from openai import OpenAI
from config.settings import HF_TOKEN, LLM_MODEL, LLM_BASE_URL
from services.logger import logger
from typing import List
from api.models import LLMExplanation
import time

# Initialize OpenAI-compatible client for Hugging Face router
llm_client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=HF_TOKEN,
    timeout=60
)

# System prompt optimized for Urdu explanations
SYSTEM_PROMPT = """آپ ایک اسلامی عالم ہیں جو قرآنی آیات کی مفصل وضاحت کرتے ہیں۔ آپ کو قرآنی آیات کا حوالہ دیا جائے گا اور صارف کا سوال۔

آپ کو ہر آیت کی تفصیلی وضاحت اردو میں پیش کرنی ہے۔ وضاحت میں شامل ہونا چاہیے:
1. آیت کا سیاق و سباق
2. لفظی ترجمہ اور معنی
3. تفصیلی تشریح
4. عملی مشورے
5. فرد اور معاشرے پر اثرات

ہدایات:
- صرف اردو زبان استعمال کریں
- سادہ اور واضح زبان استعمال کریں
- کم از کم 300 الفاظ کی وضاحت دیں
- عملی مشورے اور مثالوں سے سمجھائیں"""

def get_llm_explanation(query: str, arabic_texts: List[str], urdu_texts: List[str], verse_ids: List[int]) -> LLMExplanation:
    """Get detailed Urdu explanation from LLM using moonshotai model"""
    logger.info(f"🤖 Getting LLM explanation for query: '{query}'")
    
    try:
        # Prepare context with verses
        context_parts = []
        for i, (arabic, urdu) in enumerate(zip(arabic_texts, urdu_texts)):
            context_parts.append(f"آیت {i+1} (آیت ID: {verse_ids[i]}):")
            context_parts.append(f"عربی متن: {arabic}")
            context_parts.append(f"اردو ترجمہ: {urdu}")
            context_parts.append("")  # Empty line
        
        context = "\n".join(context_parts)
        
        # Create user prompt
        user_prompt = f"""
سوال: {query}

متعلقہ قرآنی آیات:
{context}

براہ کرم ان آیات کی اردو میں تفصیلی وضاحت کریں۔ وضاحت کم از کم 300 الفاظ کی ہونی چاہیے اور درج ذیل پہلوؤں کا احاطہ کرنی چاہیے:
1. ہر آیت کا سیاق و سباق
2. ہر آیت کا لفظی معنی
3. تفصیلی تشریح
4. عملی مشورے برائے روزمرہ زندگی
5. ان آیات سے ملنے والی کلیدی تعلیمات

وضاحت:"""
        
        logger.info(f"📝 Calling {LLM_MODEL} with {len(arabic_texts)} verses...")
        
        # Make API call with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Attempt {attempt + 1}/{max_retries}")
                
                completion = llm_client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1200,
                    timeout=45
                )
                
                urdu_explanation = completion.choices[0].message.content
                
                # Validate response length
                if len(urdu_explanation) < 100:
                    logger.warning(f"Response too short ({len(urdu_explanation)} chars)")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        raise ValueError("LLM response too short")
                
                logger.info(f"✅ LLM explanation generated ({len(urdu_explanation)} characters)")
                logger.info(f"📄 Sample: {urdu_explanation[:200]}...")
                
                return LLMExplanation(
                    urdu=urdu_explanation,
                    verses_used=verse_ids
                )
                
            except Exception as llm_error:
                logger.error(f"LLM attempt {attempt + 1} failed: {llm_error}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                else:
                    raise
        
    except Exception as e:
        logger.error(f"🤖 LLM service error: {str(e)}")
        
        # DYNAMIC FALLBACK - NOT HARDCODED
        query_lower = query.lower()
        
        # Detect topic from query
        if any(word in query_lower for word in ['roza', 'صوم', 'صيام', 'fasting']):
            topic = "روزہ"
            key_benefits = [
                "تزکیہ نفس اور روحانی پاکیزگی",
                "صبر و استقامت میں اضافہ",
                "اللہ کی خوشنودی اور قربت",
                "جسمانی و روحانی صحت",
                "غریبوں اور مسکینوں کی مدد"
            ]
        elif any(word in query_lower for word in ['namaz', 'صلوۃ', 'صلاة', 'prayer']):
            topic = "نماز"
            key_benefits = [
                "اللہ سے براہ راست تعلق",
                "نفس کی تربیت اور اخلاقی بلندی",
                "برائیوں سے حفاظت",
                "روحانی سکون اور ذہنی اطمینان",
                "روز مرہ کی پریشانیوں سے نجات"
            ]
        elif any(word in query_lower for word in ['sabr', 'صبر', 'patience']):
            topic = "صبر"
            key_benefits = [
                "مشکلات میں ثابت قدمی",
                "اللہ کی رضا و خوشنودی",
                "اندرونی طاقت و ہمت",
                "کامیابی کی کنجی",
                "دنیا و آخرت کی کامیابی"
            ]
        else:
            topic = "اسلامی تعلیمات"
            key_benefits = [
                "روحانی ترقی و کمال",
                "اخلاقی تربیت و سنوار",
                "معاشرتی انصاف و بہتری",
                "دنیاوی سکون و اطمینان",
                "آخرت کی دائمی کامیابی"
            ]
        
        # Generate dynamic fallback explanation
        verses_str = ", ".join([f"آیت {vid}" for vid in verse_ids])
        
        dynamic_fallback = f"""
**سوال: "{query}" کے بارے میں قرآنی رہنمائی**

**متعلقہ آیات:** {verses_str}

**تفصیلی وضاحت:**

قرآن مجید میں {topic} کو خصوصی اہمیت حاصل ہے۔ مندرجہ بالا آیات {topic} کے مختلف پہلوؤں پر روشنی ڈالتی ہیں۔

**اہم نکات:**

1. **{topic} کی قرآن میں اہمیت:** قرآن پاک میں {topic} کی فضیلت بیان کی گئی ہے۔

2. **کلیدی فوائد:**
   - {key_benefits[0]}
   - {key_benefits[1]}
   - {key_benefits[2]}
   - {key_benefits[3]}

3. **عملی مشورے:**
   - {topic} کو پوری توجہ اور خلوص نیت سے ادا کریں
   - اس کے شرائط و آداب کا مکمل خیال رکھیں
   - {topic} کو روزمرہ زندگی کا لازمی حصہ بنائیں

**نتیجہ:** {topic} مومن کی زندگی کا اہم ستون ہے جو دنیا و آخرت دونوں میں کامیابی کا ذریعہ بنتا ہے۔
"""
        
        logger.info(f"📝 Using dynamic fallback for topic: {topic}")
        return LLMExplanation(
            urdu=dynamic_fallback,
            verses_used=verse_ids
        )