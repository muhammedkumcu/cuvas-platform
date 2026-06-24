# -*- coding: utf-8 -*-
"""
ChuvashFST — Fonoloji Modülü (phonology.py)

Çuvaş Türkçesinin (Anatri standart) ses kurallarını tek yerde toplar.
Türkmence motorundan FARKLI: yuvarlaklık uyumu YOK, yazımsal ünsüz
yumuşaması YOK; indirgenmiş ünlü (ӑ/ӗ), gemination ve Kiril normalizasyonu VAR.

Tüm metotlar saf (stateless) fonksiyonlardır. Kurallar `kurallar/KURALLAR_CUVASCA.md`
spesifikasyonundan ve apertium-chv `.twol` dosyasından damıtılmıştır.
"""
from __future__ import annotations
import unicodedata
from typing import Optional


# ==============================================================================
#  ALFABE — ÜNLÜ VE ÜNSÜZ SİSTEMİ
# ==============================================================================

class Alphabet:
    """Çuvaş Kiril alfabesi ses sınıfları (apertium twol Sets ile uyumlu)."""

    # Art (back) ünlüler — iotated я/ё/ю dahil
    BACK_VOWELS = frozenset("аӑыоуяёю")
    # Ön (front) ünlüler
    FRONT_VOWELS = frozenset("еӗиӳэ")
    VOWELS = BACK_VOWELS | FRONT_VOWELS

    # İndirgenmiş (reduced/lax) ünlüler
    REDUCED = frozenset("ӑӗ")

    CONSONANTS = frozenset("бвгджзйклмнпрсҫтфхцчшщ")
    # Tonsuz ünsüzler (allofonik tonlulaşma; yazımda değişmez)
    VOICELESS = frozenset("птксҫчшхщц")
    # Likit + nazal — bulunma/ayrılma hallerinde т- allomorfunu tetikler
    LIQUID_NASAL = frozenset("рлн")


# ==============================================================================
#  HOMOGLYPH (görsel-aynı Latin → Kiril) NORMALİZASYONU
# ==============================================================================

# Latin harf → görsel olarak aynı Çuvaş Kiril harfi (araştırma #2, Bölüm D2)
HOMOGLYPH_MAP = {
    # küçük
    "a": "а", "c": "с", "e": "е", "o": "о", "p": "р", "x": "х", "y": "у", "k": "к",
    # büyük
    "A": "А", "B": "В", "C": "С", "E": "Е", "H": "Н", "K": "К", "M": "М",
    "O": "О", "P": "Р", "T": "Т", "X": "Х", "Y": "У",
}

# Çuvaşça'nın özel harflerinin Latin breve/sedilla karşılıkları → Kiril.
# Bazı metinler (Wikipedia dahil) Kiril ӑ/ӗ/ҫ/ӳ yerine Latin ă/ĕ/ç/ÿ kullanır;
# bu, kelimelerin morfem ortasında bölünmesine ve sahte OOV'ye yol açar.
CHUVASH_LATIN_MAP = {
    "ă": "ӑ", "ĕ": "ӗ", "ç": "ҫ", "ÿ": "ӳ", "ӱ": "ӳ",
    "Ă": "ӑ", "Ĕ": "ӗ", "Ç": "ҫ", "Ÿ": "ӳ",
}
_HOMO_TABLE = {ord(k): v for k, v in {**HOMOGLYPH_MAP, **CHUVASH_LATIN_MAP}.items()}


def normalize(text: str) -> str:
    """
    Metni morfolojik işleme için normalize eder:
      1. Unicode NFC (ayrık diyakritikleri birleşik Çuvaş karakterlerine toplar)
      2. Latin homoglyph'leri (a, e, c, o, p, x, y...) Kiril karşılıklarına çevirir

    Kiril giriş alanında kullanıcının yanlışlıkla girdiği Latin harfleri
    düzelterek sahte OOV (sözlük-dışı) durumlarını önler.
    """
    text = unicodedata.normalize("NFC", text)
    return text.translate(_HOMO_TABLE)


def has_latin_homoglyph(text: str) -> bool:
    """Metinde Latin homoglyph var mı? (uyarı/UX için)"""
    return any(ch in HOMOGLYPH_MAP for ch in text)


# ==============================================================================
#  FONOLOJİ KURALLARI
# ==============================================================================

class Phonology:
    """Çuvaşça fonotaktik kuralları — pure fonksiyonlar."""

    # -- Ünlü uyumu -----------------------------------------------------------

    @staticmethod
    def harmony(word: str) -> str:
        """
        Kelimenin son ünlüsüne göre ön/art uyumunu döndürür.
        Returns: "back" (art) | "front" (ön). Ünlü yoksa varsayılan "back".
        """
        for ch in reversed(word):
            if ch in Alphabet.BACK_VOWELS:
                return "back"
            if ch in Alphabet.FRONT_VOWELS:
                return "front"
        return "back"

    @staticmethod
    def is_front(word: str) -> bool:
        return Phonology.harmony(word) == "front"

    @staticmethod
    def V(back_variant: str, front_variant: str, word: str) -> str:
        """Uyuma göre allomorf seç (Çuvaşça'da ekler 2 varyantlı)."""
        return front_variant if Phonology.is_front(word) else back_variant

    @staticmethod
    def last_vowel(word: str) -> Optional[str]:
        for ch in reversed(word):
            if ch in Alphabet.VOWELS:
                return ch
        return None

    @staticmethod
    def ends_with_vowel(word: str) -> bool:
        return bool(word) and word[-1] in Alphabet.VOWELS

    @staticmethod
    def ends_with_reduced(word: str) -> bool:
        return bool(word) and word[-1] in Alphabet.REDUCED

    # -- Ek başı ünsüz asimilasyonu (loc/abl {T}) -----------------------------

    @staticmethod
    def takes_t_allomorph(stem: str) -> bool:
        """
        Bulunma/ayrılma hal ekleri kök р/л/н ile bitiyorsa т- ile başlar,
        aksi halde р- ile (хула→хула-ра, кӗл→кӗл-те, урам→урам-ра).
        twol: "{T} after liquids and nasals".
        """
        return bool(stem) and stem[-1] in Alphabet.LIQUID_NASAL

    @staticmethod
    def locative(stem: str) -> str:
        """Bulunma hali ekini (allomorf seçilmiş) döndürür: -ра/-ре | -та/-те."""
        if Phonology.takes_t_allomorph(stem):
            return Phonology.V("та", "те", stem)
        return Phonology.V("ра", "ре", stem)

    @staticmethod
    def ablative(stem: str) -> str:
        """Ayrılma hali eki: -ран/-рен | -тан/-тен."""
        if Phonology.takes_t_allomorph(stem):
            return Phonology.V("тан", "тен", stem)
        return Phonology.V("ран", "рен", stem)

    # -- İndirgenmiş ünlü düşmesi / bağlayıcı ünlü ----------------------------

    @staticmethod
    def drop_final_reduced(stem: str, suffix: str) -> str:
        """
        Kök-sonu indirgenmiş ünlü (ӑ/ӗ), ünlüyle başlayan ek öncesi düşer.
        twol: "Weak/stem vowel deletion". (Liste/işaret tabanlı genişletilecek.)
        """
        if not suffix or suffix[0] not in Alphabet.VOWELS:
            return stem
        if Phonology.ends_with_reduced(stem):
            return stem[:-1]
        return stem

    @staticmethod
    def connecting_vowel(stem: str) -> str:
        """Ünsüz-sonu köke bağlayıcı indirgenmiş ünlü (ă/ĕ) seç."""
        return Phonology.V("ӑ", "ӗ", stem)

    # -- Ünsüz ikizleşmesi (gemination) ---------------------------------------

    @staticmethod
    def has_geminating_shape(word: str) -> bool:
        """
        (C)VC yapısındaki tek-heceli köklerde son ünsüz, ünlü-başı ek öncesi
        ikizleşir (ҫын→ҫынн-). Pragmatik tespit: tam ünlü + tek son ünsüz.
        twol: "Consonant gemination". DOĞRULANACAK — lexicon özelliğiyle de işaretlenir.
        """
        if len(word) < 2:
            return False
        if word[-1] not in Alphabet.CONSONANTS:
            return False
        if word[-2] not in Alphabet.VOWELS:
            return False
        # tek heceli (tek tam ünlü) ve son ünlü indirgenmiş değil
        vowels = [c for c in word if c in Alphabet.VOWELS]
        return len(vowels) == 1 and word[-2] not in Alphabet.REDUCED

    @staticmethod
    def geminate_final(stem: str) -> str:
        """Kök-sonu ünsüzü ikizleştir (ҫын→ҫынн)."""
        if stem and stem[-1] in Alphabet.CONSONANTS:
            return stem + stem[-1]
        return stem
