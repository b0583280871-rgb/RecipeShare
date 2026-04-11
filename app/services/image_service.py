from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os
import uuid

#region ויראציות תמונות
def process_image_variations(original_path):
    """
    פונקציית עזר המקבלת נתיב לתמונה מקורית, מייצרת 3 וריאציות,
    שומרת אותן בדיסק ומחזירה מילון עם הנתיבים שלהן.
    """
    # 1. פתיחת התמונה המקורית בעזרת Pillow
    img = Image.open(original_path)

    # חילוץ שם הקובץ והסיומת כדי לשמור על עקביות
    folder = os.path.dirname(original_path)
    base_name = uuid.uuid4().hex  # מזהה ייחודי חדש לווריאציות

    # מילון שיכיל את הנתיבים של הווריאציות (כפי שביקשת)
    variation_paths_dict = {}

    # --- וריאציה 1: שחור-לבן דרמטי (Grayscale + Contrast) ---
    bw_img = ImageOps.grayscale(img)
    bw_img = ImageEnhance.Contrast(bw_img).enhance(1.5)
    bw_path = os.path.join(folder, f"bw_{base_name}.jpg")
    bw_img.save(bw_path)
    variation_paths_dict['bw'] = bw_path  # הוספה למילון

    # --- וריאציה 2: החלקה רכה (SMOOTH_MORE) ---
    smooth_img = img.filter(ImageFilter.SMOOTH_MORE)
    smooth_path = os.path.join(folder, f"smooth_{base_name}.jpg")
    smooth_img.save(smooth_path)
    variation_paths_dict['smooth'] = smooth_path  # הוספה למילון

    # --- וריאציה 3: חיזוק צבעים (Color Enhance) ---
    color_enhancer = ImageEnhance.Color(img)
    color_img = color_enhancer.enhance(2.0)  # מכפיל את רוויית הצבע
    color_path = os.path.join(folder, f"color_{base_name}.jpg")
    color_img.save(color_path)
    variation_paths_dict['color'] = color_path  # הוספה למילון

    # החזרת המילון המלא עם 3 הנתיבים
    return variation_paths_dict


#endregion

