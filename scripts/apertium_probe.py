# -*- coding: utf-8 -*-
"""
apertium_probe.py — Apertium FST'lerinin (turkicnlp ile) gerçekten çalıştığını KANITLAR.

Windows'ta hfst derlenmiyor; bu yüzden bunu bir LINUX ortamında çalıştır:
  - En kolay: Google Colab (ücretsiz). Yeni notebook -> bu dosyayı yapıştır -> Çalıştır.
  - Veya: WSL / Docker / herhangi bir Linux.

Amaç: apertium-chv (ve başka Türk dilleri) için analiz/stemmer/lemmatizer/üretim
çıktısını göstermek -> "kullanabiliyor muyuz?" sorusunu iddia değil KANITLA cevapla.
"""
import subprocess
import sys


def sh(cmd):
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=False)


def main():
    # 1) Kurulum (Linux'ta hfst wheel'i derlenir/yüklenir)
    sh(f"{sys.executable} -m pip install -q turkicnlp hfst")

    # 2) turkicnlp ile diller ve Apertium backend
    try:
        import turkicnlp
        print("turkicnlp sürümü:", getattr(turkicnlp, "__version__", "?"))
        try:
            from turkicnlp import list_languages
            print("Desteklenen diller:", list_languages())
        except Exception as e:
            print("list_languages hatası:", e)

        # 3) Çuvaşça Apertium FST'sini indir
        print("\n--- apertium-chv indiriliyor ---")
        turkicnlp.download("chv")

        # 4) Pipeline kur ve analiz et (stemmer + lemmatizer + etiketler)
        print("\n--- Çuvaşça analiz (apertium backend) ---")
        from turkicnlp import Pipeline
        nlp = Pipeline("chv", processors=["tokenize", "morph"],
                       morph_backend="apertium")
        text = "Эпӗ кӗнекесене вулатӑп. Ҫынсем хулара пурӑнаҫҫӗ."
        doc = nlp(text)
        for sent in getattr(doc, "sentences", [doc]):
            for tok in getattr(sent, "words", getattr(sent, "tokens", [])):
                print(" ", getattr(tok, "text", tok),
                      "->", getattr(tok, "lemma", "?"),
                      getattr(tok, "feats", getattr(tok, "tags", "?")))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\nHATA:", e)
        print("API farklı olabilir; çıktıyı paylaş, birlikte düzeltiriz.")


if __name__ == "__main__":
    main()
