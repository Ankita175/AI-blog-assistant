import base64
import streamlit as st
import google.generativeai as genai
from google.generativeai import types
from apikey import google_gemini_api_key

# Initialize the Gemini client
genai_client = genai.Client(api_key=google_gemini_api_key)

# Blog generation
def generate_blog(blog_title, keywords, num_words):
    prompt = (
        f"Write a detailed, professional, SEO-optimized blog post titled '{blog_title}'. "
        f"Include keywords naturally: {keywords}. "
        f"The blog should be about {num_words} words."
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    full_text = ""

    for chunk in genai_client.models.generate_content_stream(
        model="gemini-2.5-pro", contents=contents
    ):
        full_text += chunk.text or ""
    return full_text


# Image generation via Gemini multimodal output
def generate_images(image_prompt, num_images=1):
    image_urls = []
    for _ in range(num_images):
        response = genai_client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=f"Generate a detailed image based on: {image_prompt}. Output as base64 encoded PNG."
                        )
                    ],
                )
            ],
        )

        # Extract base64 image content if it exists
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            for part in parts:
                if part.inline_data:
                    img_data = base64.b64decode(part.inline_data.data)
                    st.image(img_data, use_container_width=True)
    return image_urls


# Streamlit Layout
st.set_page_config(layout="wide")
st.title("✍️🤖 BlogBuddy - Blog Text + Image AI Generator")
st.subheader("Generate blogs and images.")

with st.sidebar:
    st.title("Input Details")
    blog_title = st.text_input("Blog Title")
    keywords = st.text_input("Keywords (comma-separated)")
    num_words = st.slider("Word Count", 100, 2000, 500, 100)
    image_prompt = st.text_area("Image Description")
    num_images = st.number_input("Number of Images", 0, 5, 1)
    submit_button = st.button("Generate")

if submit_button:
    if not blog_title or not keywords:
        st.error("Please enter both title and keywords.")
    else:
        with st.spinner("Generating your blog and image(s) ..."):
            try:
                blog = generate_blog(blog_title, keywords, num_words)
                st.success("✅ Blog Generated Successfully!")
                st.write(blog)

                if num_images > 0 and image_prompt:
                    st.subheader("🖼️ Generated Image(s)")
                    generate_images(image_prompt, num_images)

            except Exception as e:
                st.error(f"Error occurred: {e}")
