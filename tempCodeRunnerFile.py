from lex import detect_qr_and_number
from eval import generate_output
import cv2
from color_extractor import extract_colors_after_qr


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tempCodeRunnerFile.py <image_path>")
        exit(1)
    image_path = sys.argv[1]

    print(f"Processing image: {image_path}")

    # 🖼 Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image from {image_path}")
        exit(1)

    # 🧠 Detect QR and loop number
    qr_x, loop_count = detect_qr_and_number(img)

    # Extract color sequence after the QR (if QR found, we start after it, otherwise from the start)
    if qr_x is None:
        print("No 'loop' QR code found. Returning colors in order...")
        color_sequence = extract_colors_after_qr(img, qr_x=None)  # No QR, so no x position
    else:
        print(f"Loop QR detected with loop count: {loop_count}. Returning colors with repetition...")
        color_sequence = extract_colors_after_qr(img, qr_x)  # Start after QR

        # Repeat the color sequence based on loop count
        color_sequence = color_sequence * loop_count

    # Join and print the color sequence as final output
    final_output = ' '.join(color_sequence)
    print("\nFinal Output:")
    print(final_output)
