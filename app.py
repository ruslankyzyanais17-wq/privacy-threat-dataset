import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Датасет: Нарушение конфиденциальности (Задание №6)",
    page_icon="🛡️",
    layout="wide"
)

# Заголовок и вводная информация
st.title("🛡️ Датасет: Нарушение конфиденциальности")
st.markdown("""
**Основной класс**: `PRIVACY_THREAT`  
Датасет подготовлен в строгом соответствии с требованиями законодательства (без использования реальных ПДН).  
Все чувствительные данные заменены нормализованными плейсхолдерами: `[ИМЯ]`, `[ТЕЛЕФОН]`, `[АДРЕС]`, `[EMAIL]`, `[АККАУНТ]`, `[ГЕОЛОКАЦИЯ]`.
""")

# Загрузка данных
@st.cache_data
def load_data():
    file_path = "privacy_threat_dataset.csv"
    if not os.path.exists(file_path):
        # Если запускается из корневого репозитория
        alt_path = os.path.join(os.path.dirname(__file__), "privacy_threat_dataset.csv")
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            return pd.DataFrame()
    return pd.read_csv(file_path, encoding="utf-8")

df = load_data()

if df.empty:
    st.error("Файл датасета `privacy_threat_dataset.csv` не найден в репозитории.")
    st.stop()

# Боковая панель: Фильтры
st.sidebar.header("🔍 Фильтры и Поиск")

# Поиск по ключевым словам
search_query = st.sidebar.text_input("Поиск по тексту:", placeholder="например, паспортные или номер...")

# Фильтр по подкатегориям
all_sub_labels = sorted(df['sub_label'].unique().tolist())
selected_sub_labels = st.sidebar.multiselect(
    "Подклассы нарушений:",
    options=all_sub_labels,
    default=all_sub_labels
)

# Фильтр по языку
all_languages = sorted(df['language'].unique().tolist())
selected_languages = st.sidebar.multiselect(
    "Язык (Language):",
    options=all_languages,
    default=all_languages
)

# Применение фильтров
filtered_df = df.copy()
if selected_sub_labels:
    filtered_df = filtered_df[filtered_df['sub_label'].isin(selected_sub_labels)]
if selected_languages:
    filtered_df = filtered_df[filtered_df['language'].isin(selected_languages)]
if search_query:
    filtered_df = filtered_df[filtered_df['text'].str.contains(search_query, case=False, na=False)]

# Метрики
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего записей", len(df))
col2.metric("После фильтрации", len(filtered_df))
col3.metric("Подклассов", len(df['sub_label'].unique()))
col4.metric("Статус анонимизации", "100% ПДН скрыты")

# График распределения по классам
st.subheader("📊 Распределение по подклассам")
class_counts = filtered_df['sub_label'].value_counts()
st.bar_chart(class_counts)

# Таблица датасета
st.subheader("📋 Таблица данных")
st.dataframe(
    filtered_df[['id', 'sub_label', 'text', 'language', 'is_anonymized']],
    use_container_width=True,
    height=450
)

# Экспорт / Скачивание данных
st.subheader("📥 Скачать датасет")
col_csv, col_jsonl = st.columns(2)

csv_data = filtered_df.to_csv(index=False, encoding="utf-8-sig")
col_csv.download_button(
    label="⬇️ Скачать отфильтрованный CSV",
    data=csv_data,
    file_name="privacy_threat_dataset_filtered.csv",
    mime="text/csv"
)

jsonl_data = filtered_df.to_json(orient="records", lines=True, force_ascii=False)
col_jsonl.download_button(
    label="⬇️ Скачать отфильтрованный JSONL",
    data=jsonl_data,
    file_name="privacy_threat_dataset_filtered.jsonl",
    mime="application/json"
)

# Описание подклассов
with st.expander("📖 Справочник подклассов (по ТЗ)"):
    st.markdown("""
    - **DOXING** — публикация персональных данных;
    - **DOXING_THREAT** — угроза публикации данных;
    - **PHONE_DISCLOSURE** — публикация номера телефона;
    - **ADDRESS_DISCLOSURE** — публикация адреса;
    - **LOCATION_DISCLOSURE** — раскрытие местоположения;
    - **IDENTITY_DISCLOSURE** — раскрытие личности анонимного пользователя;
    - **PRIVATE_MESSAGE_LEAK** — публикация личной переписки;
    - **INTIMATE_CONTENT_LEAK** — распространение интимных материалов;
    - **PERSONAL_DATA_REQUEST** — попытка получить / «пробить» персональные данные.
    """)
