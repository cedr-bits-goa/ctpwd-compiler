from lex import detect_qr_and_blocks
from parse import parse_blocks
from eval import generate_output
import cv2

if __name__ == "__main__":
    image_path = "./test-images/maze.jpg"

    print("Processing image...")

    img = cv2.imread(image_path)

    # 1) Detect all QRs (loop, if/else, conditions, actions, colors, maze, directions)
    blocks, loop_count, anchor_x = detect_qr_and_blocks(img)
    print("Detected blocks:", blocks)
    print("Loop count:", loop_count, "Anchor X:", anchor_x)

    # 2) Extract directions from blocks
    directions = [block["value"] for block in blocks if block.get("type") == "direction"]
    
    if directions:
        print("\n🧭 Detected Directions:")
        for direction in directions:
            print(direction)
    else:
        # 3) Parse into structure for non-direction blocks
        parsed = parse_blocks(blocks, loop_count)
        print("Parsed:", parsed)
        
        # Default behavior for other programs
        final_output = generate_output(parsed)
        print("\nFinal Output:")
        print(final_output)
