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
Датасет сформирован на основе реальных паттернов и прецедентов из открытых источников (**Telegram, ВКонтакте, WhatsApp, Reddit, X / Twitter, Discord**), но в **строгом соответствии с законодательством** (без нарушения тайны частной жизни).  
Все персональные данные заменены нормализованными токенами: `[ИМЯ]`, `[ТЕЛЕФОН]`, `[АДРЕС]`, `[EMAIL]`, `[АККАУНТ]`, `[ГЕОЛОКАЦИЯ]`.
""")

# Загрузка данных
@st.cache_data
def load_data():
    file_path = "privacy_threat_dataset.csv"
    if not os.path.exists(file_path):
        alt_path = os.path.join(os.path.dirname(__file__), "privacy_threat_dataset.csv")
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            return pd.DataFrame()
    return pd.read_csv(file_path, encoding="utf-8")

df = load_data()

if df.empty:
    st.error("Файл датасета `privacy_threat_dataset.csv` не найден.")
    st.stop()

# Боковая панель: Фильтры
st.sidebar.header("🔍 Фильтры и Поиск")

search_query = st.sidebar.text_input("Поиск по тексту:", placeholder="например, паспортные или номер...")

all_sources = sorted(df['source'].dropna().unique().tolist())
selected_sources = st.sidebar.multiselect(
    "Источник (Платформа):",
    options=all_sources,
    default=all_sources
)

all_sub_labels = sorted(df['sub_label'].unique().tolist())
selected_sub_labels = st.sidebar.multiselect(
    "Подклассы нарушений:",
    options=all_sub_labels,
    default=all_sub_labels
)

all_languages = sorted(df['language'].unique().tolist())
selected_languages = st.sidebar.multiselect(
    "Язык (Language):",
    options=all_languages,
    default=all_languages
)

# Применение фильтров
filtered_df = df.copy()
if selected_sources:
    filtered_df = filtered_df[filtered_df['source'].isin(selected_sources)]
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

# Графики распределения
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("📊 Распределение по подклассам")
    st.bar_chart(filtered_df['sub_label'].value_counts())
with col_g2:
    st.subheader("🌐 Распределение по платформам-источникам")
    st.bar_chart(filtered_df['source'].value_counts())

# Таблица датасета
st.subheader("📋 Таблица данных с указанием источников")
st.dataframe(
    filtered_df[['id', 'sub_label', 'source', 'text', 'language', 'is_anonymized']],
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

# Описание источников и законности
with st.expander("🌐 Описание открытых источников и соблюдения законодательства"):
    st.markdown("""
    ### Откуда взяты данные:
    1. **Telegram**: публичные каналы сливов, чаты жильцов ЖК, каналы деанонимизации, чаты ОСИНТ и сервисов «пробива».
    2. **ВКонтакте (VK)**: открытые комментарии городских пабликов («Подслушано», «Черный список»), группы поиска должников.
    3. **WhatsApp**: открытые публичные чаты и чаты объявлений, пересылаемые тексты угроз от нелегальных взыскателей.
    4. **Reddit**: публичные сабреддиты по расследованиям киберугроз (`r/doxxing`, `r/Scams`, `r/OSINT`).
    5. **X (Twitter)** & **Discord**: открытые треды кибербуллинга, разглашения закрытых номеров и утечек переписок.
    6. **Тематические форумы**: архивы открытых инцидентов утечек баз данных.

    ### Как обеспечивается законность (152-ФЗ / GDPR):
    В оригинальных сообщениях из этих источников содержались реальные номера телефонов, адреса и имена реальных людей. Публикация таких данных нарушает закон о персональных данных и ст. 137 УК РФ (нарушение неприкосновенности частной жизни).  
    Поэтому все персональные данные были **обезличены и заменены на нормализованные токены**:
    `[ИМЯ]`, `[ТЕЛЕФОН]`, `[АДРЕС]`, `[EMAIL]`, `[АККАУНТ]`, `[ГЕОЛОКАЦИЯ]`.  
    Датасет полностью легален и готов для академического использования и машинного обучения.
    """)
