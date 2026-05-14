from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import webbrowser
import urllib.parse

class DriveMate(BoxLayout):
    status = StringProperty("Ready")

    def add_trip(self):
        try:
            destination = self.ids.destination.text.strip()
            start_km = float(self.ids.start_km.text)
            end_km = float(self.ids.end_km.text)
            fuel_price = float(self.ids.fuel_price.text)
            km_per_litre = float(self.ids.km_per_litre.text)
            notes = self.ids.notes.text.strip()

            distance = end_km - start_km
            fuel_cost = (distance / km_per_litre) * fuel_price

            store = JsonStore("trips.json")
            key = datetime.now().strftime("%Y%m%d%H%M%S")

            store.put(key,
                date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                destination=destination,
                start_km=start_km,
                end_km=end_km,
                distance=round(distance, 2),
                fuel_cost=round(fuel_cost, 2),
                notes=notes
            )

            self.status = f"Saved: {distance:.2f} km | Fuel R{fuel_cost:.2f}"
            self.ids.destination.text = ""
            self.ids.start_km.text = ""
            self.ids.end_km.text = ""
            self.ids.notes.text = ""

        except Exception:
            self.status = "Error: check your numbers"

    def open_waze(self):
        destination = self.ids.destination.text.strip()
        if not destination:
            self.status = "Enter destination first"
            return

        encoded = urllib.parse.quote(destination)
        url = f"https://waze.com/ul?q={encoded}&navigate=yes"
        webbrowser.open(url)
        self.status = "Opening Waze..."

class TerriDriveMateApp(App):
    def build(self):
        return DriveMate()

if __name__ == "__main__":
    TerriDriveMateApp().run()
