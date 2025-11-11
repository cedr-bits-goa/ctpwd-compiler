# lex.py
import re
import cv2
import pytesseract
from pyzbar.pyzbar import decode

# --- Constants (extend these as needed) ---
CONTROL_SET = {"if", "else", "elseif", "else if"}   # support "else if"
CONDITION_SET = {"raining", "sunny", "snowing", "green", "red"}
ACTION_SET = {"umbrella", "sunglasses", "coat", "go", "stop"}
COLOR_WORDS = {
    "red", "blue", "green", "yellow", "orange", "purple", "pink",
    "brown", "black", "white", "cyan", "magenta", "grey", "gray"
}
DIRECTION_SET = {"up", "down", "left", "right"}



# --- Helpers ---
def _safe_crop_right(image, x, y, w, h, extra_right=80):
    H, W = image.shape[:2]
    x1 = x + w
    x2 = min(x + w + extra_right, W)
    if x2 <= x1:
        return None
    y1 = max(y, 0)
    y2 = min(y + h, H)
    if y2 <= y1:
        return None
    return image[y1:y2, x1:x2]


def _read_number_from_region(region):
    """Use Tesseract to extract a digit from the cropped region."""
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=config).strip()
    return int(text) if text.isdigit() else None


def _normalize_qr_text(raw_text: str) -> str:
    """Lowercase and strip non-alphanumeric characters (keep spaces)."""
    if raw_text is None:
        return ""
    s = raw_text.strip().lower()
    s = re.sub(r'[^a-z0-9 ]+', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _classify_qr_text(text, x, y, w, h, image):
    """Classify normalized QR content into block type and extract values if needed."""
    text = _normalize_qr_text(text)

    # Normalize "else if" -> "elseif"
    if text == "else if":
        text = "elseif"

    if text == "loop":
        region = _safe_crop_right(image, x, y, w, h, extra_right=80)
        loop_count = _read_number_from_region(region) if region is not None else None
        return {"type": "loop", "value": loop_count or 1}, x + w + 80

    if text in CONTROL_SET:
        return {"type": "control", "value": text}, x + w

    if text in CONDITION_SET:
        return {"type": "condition", "value": text}, x + w

    if text in ACTION_SET:
        return {"type": "action", "value": text}, x + w

    if text in COLOR_WORDS:
        return {"type": "color", "value": text}, x + w

    if text == "maze":
        return {"type": "maze", "value": "maze"}, x + w

    if text in DIRECTION_SET:
        return {"type": "direction", "value": text}, x + w

    # Fallback: generic label
    return {"type": "label", "value": text}, x + w


# --- Main function ---
def detect_qr_and_blocks(image):
    """Detect QR codes in an image and classify them into compiler blocks."""
    qr_codes = list(decode(image))
    if not qr_codes:
        return [], 1, None

    qr_codes.sort(key=lambda q: q.rect.left)

    blocks = []
    loop_count = 1
    anchor_x = 0

    for qr in qr_codes:
        qr_text = qr.data.decode("utf-8", errors="ignore")
        x, y, w, h = qr.rect

        block, right_edge = _classify_qr_text(qr_text, x, y, w, h, image)
        blocks.append(block)

        if block["type"] == "loop":
            loop_count = block["value"]

        anchor_x = max(anchor_x, right_edge)

    return blocks, loop_count, (anchor_x if anchor_x > 0 else None)
