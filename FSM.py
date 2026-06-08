from engine import FashionEngine

class FashionFSM:

    def __init__(self):
        self.state = "START"
        self.engine = FashionEngine()
        self.selections = {
            "event": None,
            "weather": None,
            "gender": None,
            "color": None
        }

    def process(self, user_input):
        intent = self.engine.detect_intent(user_input)

        if self.state == "START":
            if intent == "greeting":
                self.state = "GREETING"
                return {
                    "text": (
                        "Halo 👋\n"
                        "Saya FashionBot.\n"
                        "Ketik outfit untuk mendapatkan rekomendasi."
                    ),
                    "image": None
                }
            return {"text": "Silakan ketik Halo terlebih dahulu.", "image": None}

        elif self.state == "GREETING":
            if intent == "outfit":
                self.state = "ASK_EVENT"
                return {"text": self.engine.print_menu(), "image": None}
            return {"text": "Ketik outfit untuk melanjutkan.", "image": None}

        elif self.state == "ASK_EVENT":
            if intent in ["kampus", "kerja", "pesta", "nongkrong", "seminar"]:
                self.selections["event"] = intent
                self.state = "ASK_WEATHER"
                return {"text": "Bagaimana cuacanya saat ini? (Panas / Dingin)", "image": None}
            return {"text": "Pilih kampus, kerja, pesta, nongkrong, atau seminar.", "image": None}

        elif self.state == "ASK_WEATHER":
            if intent in ["panas", "dingin"]:
                self.selections["weather"] = intent
                self.state = "ASK_GENDER"
                return {"text": "Pilih gender Anda untuk gaya pakaian:", "image": None}
            return {"text": "Pilih cuaca saat ini: panas atau dingin.", "image": None}

        elif self.state == "ASK_GENDER":
            if intent in ["pria", "wanita"]:
                self.selections["gender"] = intent
                self.state = "ASK_COLOR"
                return {"text": "Pilih warna pakaian favorit Anda (Putih / Hitam):", "image": None}
            return {"text": "Pilih gender Anda: pria atau wanita.", "image": None}

        elif self.state == "ASK_COLOR":
            if intent in ["putih", "hitam"]:
                self.selections["color"] = intent
                self.state = "SHOW_OUTFIT"
                return self.get_recommendation()
            return {"text": "Pilih warna pakaian favorit Anda: putih atau hitam.", "image": None}

        elif self.state == "SHOW_OUTFIT":
            if intent == "end":
                self.state = "ASK_LOOP"
                return {"text": "Ingin memilih outfit lainnya?", "image": None}
            return {"text": "Ketik selesai untuk mengakhiri percakapan.", "image": None}

        elif self.state == "ASK_LOOP":
            if intent == "yes":
                # Reset selections but preserve saved_outfits in Streamlit session_state
                self.selections = {
                    "event": None,
                    "weather": None,
                    "gender": None,
                    "color": None
                }
                self.state = "ASK_EVENT"
                return {"text": "Baik! Mari pilih outfit lainnya.\n\n" + self.engine.print_menu(), "image": None}
            elif intent in ["no", "end"]:
                self.state = "END"
                return {"text": "Terima kasih telah menggunakan FashionBot. Percakapan selesai.", "image": None}
            return {"text": "Pilih 'ingin' atau 'tidak'.", "image": None}

        return {"text": "Percakapan selesai.", "image": None}

    def get_recommendation(self):
        event = self.selections["event"]
        weather = self.selections["weather"]
        gender = self.selections["gender"]
        color = self.selections["color"]

        gnd_name = "Pria" if gender == "pria" else "Wanita"
        col_name = color.capitalize()
        
        # Custom items based on combination
        if event == "kampus":
            title = f"🎓 Outfit Kampus ({gnd_name})"
            if gender == "pria":
                items = [f"Kaos {col_name} Katun", "Celana Chino Khaki", f"Sneakers {col_name} Minimalis"]
            else:
                items = [f"Kaos/Blouse {col_name}", "Celana Jeans Biru", f"Sneakers {col_name} Canvas"]
                
        elif event == "kerja":
            title = f"💼 Outfit Kerja ({gnd_name})"
            if gender == "pria":
                items = [f"Kemeja {col_name} Slimfit", "Celana Bahan Hitam", "Sepatu Pantofel Kulit"]
            else:
                items = [f"Kaos/Blouse {col_name}", "Celana Jeans Biru", f"Sneakers {col_name} Canvas"]
                
        elif event == "pesta":
            title = f"🎉 Outfit Pesta ({gnd_name})"
            if gender == "pria":
                if color == "putih":
                    items = [f"Kaos {col_name} Katun", "Celana Chino Khaki", f"Sneakers {col_name} Minimalis"]
                else:
                    items = [f"Kaos {col_name} Oversized (Graphic)", "Celana Cargo Hijau Olive", "Sneakers Premium Retro"]
            else:
                items = [f"Kaos/Blouse {col_name}", "Celana Jeans Biru", f"Sneakers {col_name} Canvas"]

        elif event == "nongkrong":
            title = f"☕ Outfit Nongkrong ({gnd_name})"
            if gender == "pria":
                items = [f"Kaos {col_name} Katun", "Celana Chino Khaki", f"Sneakers {col_name} Minimalis"]
            else:
                items = [f"Kaos/Blouse {col_name}", "Celana Jeans Biru", f"Sneakers {col_name} Canvas"]

        elif event == "seminar":
            title = f"📝 Outfit Seminar ({gnd_name})"
            if gender == "pria":
                items = [f"Kemeja {col_name} Slimfit", "Celana Bahan Hitam", "Sepatu Pantofel Kulit"]
            else:
                items = [f"Kaos/Blouse {col_name}", "Celana Jeans Biru", f"Sneakers {col_name} Canvas"]
                
        # Adjust for weather
        weather_note = ""
        if weather == "dingin":
            weather_note = "\n🧥 *Tip Cuaca Dingin:* Tambahkan Jaket/Sweater luar agar tetap hangat!"
        else:
            weather_note = "\n☀️ *Tip Cuaca Panas:* Gunakan bahan katun tipis yang menyerap keringat."
            
        items_str = "\n".join([f"✅ {item}" for item in items])
        
        text = f"""{title}

{items_str}
{weather_note}
"""
        
        # Image name format: assets/{event}_{gender}_{color}.png
        image_path = f"assets/{event}_{gender}_{color}.png"
        
        return {"text": text, "image": image_path}