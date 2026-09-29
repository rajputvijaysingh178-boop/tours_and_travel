from urllib.parse import urlparse


def normalize_images(images) -> list[dict]:
    if not images:
        return []

    normalized = []

    for item in images:
        if isinstance(item, str):
            url = item.strip()
            public_id = ""
            alt = ""
        elif isinstance(item, dict):
            url = str(item.get("url") or "").strip()
            public_id = str(item.get("public_id") or "").strip()
            alt = str(item.get("alt") or "").strip()
        else:
            raise ValueError("Invalid image payload")

        if not url:
            continue

        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != "res.cloudinary.com":
            raise ValueError(
                "Image URL must be an HTTPS Cloudinary URL (res.cloudinary.com)"
            )

        normalized.append({
            "url": url,
            "public_id": public_id,
            "alt": alt,
        })

    return normalized


def first_image_url(images) -> str | None:
    if not images:
        return None
    first = images[0]
    if isinstance(first, dict):
        return first.get("url")
    return str(first)
