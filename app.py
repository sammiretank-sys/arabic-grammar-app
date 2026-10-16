import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="مساعد اللغة العربية والإعراب",
    page_icon="📚",
    layout="centered"
)

st.title("مساعد النحو والإعراب الذكي 📚")
st.write("هذا التطبيق مخصص لمساعدتك في إعراب الجمل العربية وتحليلها بدقة عالية باستخدام الذكاء الاصطناعي.")

# قراءة المفتاح تلقائياً من Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات Streamlit Secrets.")
    st.stop()

# إعداد الـ API
genai.configure(api_key=api_key)

user_input = st.text_area("أدخل الجملة أو النص المراد إعرابه:")

if st.button("إعراب وتحليل النص"):
    if not user_input.strip():
        st.warning("الرجاء كتابة جملة واحدة على الأقل.")
    else:
        with st.spinner("جاري تحليل الإعراب والقواعد..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"قم بإعراب الجملة التالية إعراباً تفصيلياً كاملاً مع توضيح القواعد النحوية: {user_input}"
                response = model.generate_content(prompt)
                
                st.success("تم الإعراب بنجاح!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}")
