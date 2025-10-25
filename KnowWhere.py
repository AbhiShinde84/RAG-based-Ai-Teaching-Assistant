import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
from sklearn.metrics.pairwise import cosine_similarity



def create_embedding(text_list):
    """Create embeddings using Ollama bge-m3 model."""
    try:
        r = requests.post("http://localhost:11434/api/embed", json={
            "model": "bge-m3",
            "input": text_list
        })
        r.raise_for_status()
        return r.json()["embeddings"]
    except Exception as e:
        st.error(f"Embedding error: {e}")
        return None


def inference(prompt):
    """Generate answer using Llama 3.2 model from Ollama."""
    try:
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        })
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        st.error(f"Inference error: {e}")
        return "Error generating response."



st.set_page_config(page_title="AI Teaching Assistant", page_icon="🎓", layout="wide")

st.title("🎓 AI Teaching Assistant (RAG-based)")
st.markdown(
    """
    Ask questions about your **Sigma Web Development course** videos.
    The assistant will tell you **where (video + timestamp)** a topic was covered and give you a helpful explanation.  
    """
)

# Load saved embeddings
@st.cache_resource
def load_embeddings():
    try:
        df = joblib.load("embeddings.joblib")
        return df
    except FileNotFoundError:
        st.error("❌ embeddings.joblib not found. Please generate and save it first.")
        st.stop()

df = load_embeddings()

# User input
incoming_query = st.text_input("💬 Ask your question here:")

if st.button("Get Answer"):
    if not incoming_query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing your question and retrieving relevant content..."):
            # Step 1: Create query embedding
            query_embedding = create_embedding([incoming_query])[0]

            # Step 2: Compute cosine similarity
            similarities = cosine_similarity(np.vstack(df["embedding"]), [query_embedding]).flatten()
            top_results = 5
            max_indx = similarities.argsort()[::-1][0:top_results]

            new_df = df.loc[max_indx]

            # Step 3: Relevance threshold
            if max(similarities) < 0.45:
                st.warning("❌ The question seems unrelated to the course.")
            else:
                # Step 4: Construct prompt
                video_chunks_json = new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")

                prompt = f"""
                I am teaching web development in my Sigma web development course. 
                Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:
                {video_chunks_json}
                ---------------------------------
                "{incoming_query}"
                The user asked this question related to the video chunks. 
                Answer in a clear, human way without mentioning the above format. 
                Tell which video (and timestamps) cover the topic and guide the user to that video.
                If unrelated, say you can only answer course-related questions.
                """

                # Save prompt for debugging
                with open("prompt.txt", "w", encoding="utf-8") as f:
                    f.write(prompt)

                # Step 5: Generate response
                response = inference(prompt)

                # Save response
                with open("response.txt", "w", encoding="utf-8") as f:
                    f.write(response)

                # Step 6: Display results
                st.success("✅ Answer generated successfully!")
                st.subheader("🧠 AI Assistant Response:")
                st.write(response)

                # Step 7: Show top matching video chunks
                with st.expander("🎬 Relevant Video Segments"):
                    for _, row in new_df.iterrows():
                        st.markdown(
                            f"**🎥 {row['title']} (Video {row['number']})**  "
                            f"🕒 {int(row['start'])}s - {int(row['end'])}s  \n"
                            f"> {row['text'][:300]}..."
                        )
