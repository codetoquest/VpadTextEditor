import re
from collections import Counter
from typing import List

_STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'to', 'of', 'in', 'on', 'for', 'with',
    'as', 'at', 'by', 'is', 'are', 'was', 'were', 'be', 'this', 'that', 'it', 'from',
    'we', 'you', 'they', 'i', 'our', 'your', 'their', 'will', 'can', 'should', 'could'
}


def _split_sentences(text: str) -> List[str]:
    cleaned = text.strip()
    if not cleaned:
        return []
    parts = re.split(r'(?<=[.!?])\s+', cleaned)
    return [part.strip() for part in parts if part.strip()]


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Create a lightweight extractive summary from raw text."""
    sentences = _split_sentences(text)
    if not sentences:
        return 'No content to summarize.'

    words = re.findall(r"[a-zA-Z']+", text.lower())
    frequencies = Counter(word for word in words if word not in _STOP_WORDS and len(word) > 2)

    if not frequencies:
        return ' '.join(sentences[:max_sentences])

    ranked = []
    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(r"[a-zA-Z']+", sentence.lower())
        score = sum(frequencies[word] for word in sentence_words)
        ranked.append((score, index, sentence))

    top = sorted(ranked, key=lambda item: item[0], reverse=True)[:max_sentences]
    ordered = sorted(top, key=lambda item: item[1])
    return ' '.join(sentence for _, _, sentence in ordered)


def _extract_candidate_items(text: str) -> List[str]:
    """Collect task-like items from lines and sentences."""
    cues = ('todo', 'fix', 'add', 'implement', 'update', 'refactor', 'review', 'ship', 'test')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    candidates: List[str] = []

    for line in lines:
        plain = re.sub(r'^[-*\d.)\s]+', '', line).strip()
        if not plain:
            continue

        line_sentences = _split_sentences(plain) or [plain]
        for sentence in line_sentences:
            clean_sentence = sentence.strip()
            low = clean_sentence.lower()

            if low.startswith(cues) or any(marker in low for marker in ('todo:', 'action:', 'next:')):
                candidates.append(clean_sentence)
                continue

            if re.search(r'\b(need to|should|must|let\'s|please)\b', low):
                candidates.append(clean_sentence)

    return candidates


def extract_action_items(text: str) -> str:
    """Extract likely action items using imperative and TODO-like cues."""
    candidates = _extract_candidate_items(text)

    unique_items = []
    seen = set()
    for item in candidates:
        normalized = item.lower().rstrip('.!')
        if normalized not in seen:
            unique_items.append(item.rstrip())
            seen.add(normalized)

    if not unique_items:
        return 'No obvious action items found.'

    return '\n'.join(f'- [ ] {item.rstrip(".!")}' for item in unique_items)


def improve_clarity(text: str) -> str:
    """Apply deterministic clarity improvements without external services."""
    if not text.strip():
        return text

    replacements = {
        r'\butilize\b': 'use',
        r'\bin order to\b': 'to',
        r'\bdue to the fact that\b': 'because',
        r'\bat this point in time\b': 'now',
        r'\bvery\s+': '',
    }

    refined = text
    for pattern, replacement in replacements.items():
        refined = re.sub(pattern, replacement, refined, flags=re.IGNORECASE)

    refined = re.sub(r'\s+', ' ', refined).strip()
    return refined


def to_bullet_points(text: str) -> str:
    sentences = _split_sentences(text)
    if not sentences:
        return 'No content to convert.'
    return '\n'.join(f'• {sentence.rstrip(".")}' for sentence in sentences)
