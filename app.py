import streamlit as st
from PIL import Image, UnidentifiedImageError
import pillow_heif
import io

# Register HEIF/HEIC plugin
pillow_heif.register_heif_opener()

st.set_page_config(page_title="Universal Image to PDF", layout="centered")
st.title("🖼️ Convert Any Image to PDF")
st.write("Upload images of any format (JPG, PNG, HEIC, BMP, TIFF, WEBP, etc.). Each image becomes a PDF page.")

uploaded_files = st.file_uploader(
    "Upload Images",
    type=None,  # Accept all formats
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 200:
        st.warning("⚠️ You uploaded more than 200 files. Only the first 200 will be processed.")
        uploaded_files = uploaded_files[:200]

    if st.button("Convert to PDF"):
        images = []

        for file in uploaded_files:
            try:
                img = Image.open(file)
                img = img.convert("RGB")
                images.append(img)
            except UnidentifiedImageError:
                st.error(f"❌ Could not read image: {file.name} — unsupported or corrupted.")
            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {e}")

        if images:
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format='PDF', save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            st.success("✅ PDF created successfully!")
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="converted.pdf",
                mime="application/pdf"
            )
        else:
            st.error("⚠️ No valid images to convert.")
