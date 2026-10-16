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
            
            # استخدام الرابط المباشر مع مفتاح كـ query parameter
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(url, json=payload, headers=headers)
                data = response.json()

                if response.status_code == 200:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    st.success("تم الإعراب بنجاح!")
                    st.write(text)
                else:
                    error_msg = data.get('error', {}).get('message', 'حدث خطأ غير معروف')
                    st.error(f"خطأ من الخدمة ({response.status_code}): {error_msg}")
                        
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}")
