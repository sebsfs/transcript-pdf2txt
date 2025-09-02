import copy

def is_rotated_bbox(pages, threshold_ratio=0.7):
    vertical = 0
    horizontal = 0

    for page in pages:
        for item in page.get("results", []):
            bbox = item.get("bbox")
            if not bbox:
                continue
            width = bbox["x_max"] - bbox["x_min"]
            height = bbox["y_max"] - bbox["y_min"]
            if height > width:
                vertical += 1
            else:
                horizontal += 1

    total = vertical + horizontal
    return vertical / total > threshold_ratio if total else False

def rotate_bbox_90_ccw(bbox, page_width, page_height):
    corners = [
        (bbox["x_min"], bbox["y_min"]),
        (bbox["x_max"], bbox["y_min"]),
        (bbox["x_max"], bbox["y_max"]),
        (bbox["x_min"], bbox["y_max"]),
    ]

    rotated = [(y, page_width - x) for (x, y) in corners]

    xs = [pt[0] for pt in rotated]
    ys = [pt[1] for pt in rotated]

    return {
        "x_min": int(min(xs)),
        "y_min": int(min(ys)),
        "x_max": int(max(xs)),
        "y_max": int(max(ys))
    }

def correct_if_rotated(pages):
    if not pages:
        return pages

    # Estimar tamaño máximo de página
    max_x = max(item["bbox"]["x_max"] for page in pages for item in page["results"])
    max_y = max(item["bbox"]["y_max"] for page in pages for item in page["results"])

    page_width = max_x
    page_height = max_y

    if not is_rotated_bbox(pages):
        return pages

    corrected = copy.deepcopy(pages)

    for page in corrected:
        for item in page["results"]:
            if "bbox" in item:
                item["bbox"] = rotate_bbox_90_ccw(item["bbox"], page_width, page_height)

    return corrected

