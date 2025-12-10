import base64
import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import os


# Get API key (use environment variable for Streamlit Cloud)
google_gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')


# Configure Gemini
genai.configure(api_key=google_gemini_api_key)


# Blog generation
def generate_blog(blog_title, keywords, num_words):
    prompt = (
        f"Write a detailed, professional, SEO-optimized blog post titled '{blog_title}'. "
        f"Include keywords naturally: {keywords}. "
        f"The blog should be about {num_words} words."
    )

    model = genai.GenerativeModel('gemini-pro')
    
    # Generate content with streaming
    response = model.generate_content(prompt, stream=True)
    full_text = ""
    
    for chunk in response:
        full_text += chunk.text or ""
    
    return full_text


# Image generation via Gemini multimodal output
def generate_images(image_prompt, num_images=1):
    image_urls = []
    model = genai.GenerativeModel('gemini-pro')
    
    for _ in range(num_images):
        try:
            response = model.generate_content(
                f"Generate a detailed image based on: {image_prompt}. Output as base64 encoded PNG."
            )
            
            # Note: Gemini Pro doesn't generate actual images
            # This is a text-based response
            st.info("Note: Gemini Pro generates text descriptions, not actual images.")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Image generation error: {e}")
    
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
