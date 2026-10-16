import streamlit as st
import google.generativeai as genai

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="مساعد اللغة العربية والإعراب",
    page_icon="📚",
    layout="centered"
)

st.title("📚 مساعد النحو والإعراب الذكي")
st.write("هذا التطبيق مخصص لمساعدتك في إعراب الجمل العربية وتحليلها بدقة عالية باستخدام الذكاء الاصطناعي.")

# إدخال مفتاح الـ API الخاص بـ Google Gemini
api_key = st.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")

if not api_key:
    st.info("الرجاء إدخال مفتاح Google Gemini API للبدء. يمكنك الحصول عليه مجاناً من Google AI Studio.")
    st.stop()

# إعداد نموذج الذكاء الاصطناعي
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
# إدخال النص من المستخدم
user_input = st.text_area("أدخل الجملة أو النص المراد إعرابه:")

if st.button("إعراب وتحليل النص"):
    if user_input.strip() == "":
        st.warning("الرجاء كتابة جملة واحدة على الأقل.")
    else:
        with st.spinner("جاري تحليل الإعراب والقواعد..."):
            try:
                # توجيه النموذج ليعمل كخبير نحوي
                prompt = f"""
                أنت أستاذ خبير في النحو والصرف العربي. قم بإعراب الجملة التالية إعراباً مفصلاً ودقيقاً مع ذكر السبب والعلامة الإعرابية لكل كلمة:
                الجملة: {user_input}
                """
                response = model.generate_content(prompt)
                
                st.subheader("نتيجة الإعراب:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ ما: {e}")
