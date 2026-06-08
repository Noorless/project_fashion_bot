import re

class FashionEngine:

    def detect_intent(self, text):

        text = text.lower()

        if re.search(r"\b(halo|hai|hi)\b", text):
            return "greeting"

        elif re.search(r"\b(outfit|fashion|pakaian)\b", text):
            return "outfit"

        elif re.search(r"\b(kampus)\b", text):
            return "kampus"

        elif re.search(r"\b(kerja)\b", text):
            return "kerja"

        elif re.search(r"\b(pesta)\b", text):
            return "pesta"

        elif re.search(r"\b(nongkrong|hangout|santai|main)\b", text):
            return "nongkrong"

        elif re.search(r"\b(seminar|presentasi|sidang)\b", text):
            return "seminar"

        elif re.search(r"\b(panas|hujan|cerah|terang)\b", text):
            return "panas"

        elif re.search(r"\b(dingin|salju|mendung|sejuk)\b", text):
            return "dingin"

        elif re.search(r"\b(pria|laki-laki|cowo|cowok|l)\b", text):
            return "pria"

        elif re.search(r"\b(wanita|perempuan|cewe|cewek|p)\b", text):
            return "wanita"

        elif re.search(r"\b(putih)\b", text):
            return "putih"

        elif re.search(r"\b(hitam)\b", text):
            return "hitam"

        elif re.search(r"\b(ingin|mau|ya|yes|y)\b", text):
            return "yes"

        elif re.search(r"\b(tidak|no|t|tidak mau|nggak|g)\b", text):
            return "no"

        elif re.search(r"\b(selesai|bye)\b", text):
            return "end"

        return "unknown"

    def parse_single_segment(self, text):
        return text.lower().strip()

    def parse_orders(self, text):
        return text.split(",")

    def print_menu(self):

        return """
Pilih kebutuhan outfit:

- kampus
- kerja
- pesta
- nongkrong
- seminar
"""