import streamlit as st
import requests

st.set_page_config(
    page_title="مساعد اللغة العربية والإعراب",
    page_icon="📚",
    layout="centered"
)

st.title("مساعد النحو والإعراب الذكي 📚")
st.write("هذا التطبيق مخصص لمساعدتك في إعراب الجمل العربية وتحليلها بدقة عالية باستخدام الذكاء الاصطناعي.")

api_key_input = st.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")
user_input = st.text_area("أدخل الجملة أو النص المراد إعرابه:")

if st.button("إعراب وتحليل النص"):
    key = api_key_input.strip()
    if not key:
        st.error("الرجاء إدخال مفتاح الـ API أولاً.")
    elif not user_input.strip():
        st.warning("الرجاء كتابة جملة واحدة على الأقل.")
    else:
        with st.spinner("جاري تحليل الإعراب والقواعد..."):
            prompt = f"قم بإعراب الجملة التالية إعراباً تفصيلياً كاملاً مع توضيح القواعد النحوية: {user_input}"
            
            # إعداد الطلب
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            headers = {"Content-Type": "application/json"}
            
            # إذا كان المفتاح ينتهي/يبدأ بـ AQ يتم إرساله كـ Bearer
            if key.startswith("AQ"):
                headers["Authorization"] = f"Bearer {key}"
                params = {}
            else:
                params = {"key": key}

            try:
                response = requests.post(url, json=payload, headers=headers, params=params)
                data = response.json()

                if response.status_code == 200:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("تم الإعراب بنجاح!")
                    st.write(text)
                else:
                    error_msg = data.get('error', {}).get('message', 'حدث خطأ غير معروف')
                    st.error(f"خطأ من الخدمة ({response.status_code}): {error_msg}")
                    if "UNAUTHENTICATED" in str(data) or "401" in str(response.status_code):
                        st.info("ملاحظة: ينصح باستخدام مفتاح يبدأ بـ AIzaSy من Google AI Studio.")
                        
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}")
