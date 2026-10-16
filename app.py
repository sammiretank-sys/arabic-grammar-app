import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="مساعد اللغة العربية والإعراب",
    page_icon="📚",
    layout="centered"
)

st.title("مساعد النحو والإعراب الذكي 📚")
st.write("هذا التطبيق مخصص لمساعدتك في إعراب الجمل العربية وتحليلها بدقة عالية باستخدام الذكاء الاصطناعي.")

# حقل إدخال المفتاح
api_key_input = st.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")

user_input = st.text_area("أدخل الجملة أو النص المراد إعرابه:")

if st.button("إعراب وتحليل النص"):
    key = api_key_input.strip()
    if not key:
        st.error("الرجاء إدخال مفتاح الـ API أولاً.")
    elif not user_input.strip():
        st.warning("الرجاء كتابة جملة واحدة على الأقل.")
    else:
        with st.spinner("جاري تحليل الإعراب والقواعد..."):
            try:
                # تعيين المفتاح كمتبيئة نظام مؤقتة لضمان قراءته من المكتبة مباشرة
                os.environ["GEMINI_API_KEY"] = key
                
                # تهيئة العميل بالطريقة القياسية
                client = genai.Client()
                
                prompt = f"قم بإعراب الجملة التالية إعراباً تفصيلياً كاملاً مع توضيح القواعد النحوية: {user_input}"
                
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
                
                st.success("تم الإعراب بنجاح!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}")
