import os
from PIL import Image
import streamlit as st

def resize_image_or_images(input_path, output_dir, new_width, new_height):
    """
    Resizes an individual image or all images in a directory and saves them in the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isdir(input_path):
        st.write("Processing directory...")
        for file_name in os.listdir(input_path):
            input_file_path = os.path.join(input_path, file_name)

            # Resize each image in the directory
            try:
                with Image.open(input_file_path) as img:
                    resized_img = img.resize((new_width, new_height))
                    output_file_path = os.path.join(output_dir, file_name)
                    resized_img.save(output_file_path)
            except Exception as e:
                st.warning(f"Skipping {file_name}: {e}")
    elif os.path.isfile(input_path):
        try:
            st.write(f"Processing: {os.path.basename(input_path)}")
            with Image.open(input_path) as img:
                file_name = os.path.basename(input_path)
                resized_img = img.resize((new_width, new_height))
                output_file_path = os.path.join(output_dir, file_name)
                resized_img.save(output_file_path)
        except Exception as e:
            st.error(f"Could not process the file: {input_path}\n{e}")
    else:
        st.error(f"Invalid path: {input_path}")
    st.success("Processing completed!")

# Streamlit interface
st.title("Unique Image Resizer")

# File uploader for input
uploaded_file = st.file_uploader("Upload an image or zip folder", type=["jpg", "jpeg", "png", "zip"])
input_path = None

if uploaded_file:
    input_path = os.path.join("uploads", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(input_path, caption="Uploaded Image", use_column_width=True)

# Select output directory
output_dir = st.text_input("Enter output directory path:")
if st.button("Create Output Directory"):
    os.makedirs(output_dir, exist_ok=True)
    st.success(f"Output directory {output_dir} is ready.")

# Set new dimensions
col1, col2 = st.columns(2)
new_width = col1.number_input("New Width", min_value=1, step=1)
new_height = col2.number_input("New Height", min_value=1, step=1)

# Start resizing
if st.button("Start Resizing"):
    if not input_path:
        st.error("Please upload an image or zip folder.")
    elif not output_dir:
        st.error("Please provide an output directory.")
    elif new_width <= 0 or new_height <= 0:
        st.error("Width and height must be greater than zero.")
    else:
        resize_image_or_images(input_path, output_dir, int(new_width), int(new_height))
