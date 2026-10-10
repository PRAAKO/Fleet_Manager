from datetime import date
import json
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

DATA_FILE = "fleet_accounts.json"


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
      data = json.load(f)
      if "vehicles" not in data and "drivers" not in data:
        return {"vehicles": data, "drivers": {}}
      return data
  return {"vehicles": {}, "drivers": {}}


def save_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


# --- Screens Logic ---
class MenuScreen(Screen):
  pass


class VehicleExpenseScreen(Screen):

  def save_veh_expense(self, veh_input, amt_input, note_input, status_label):
    veh = veh_input.text.upper().strip()
    amt_str = amt_input.text.strip()
    note = note_input.text.strip()

    if not veh:
      status_label.text = "❌ Error: Vehicle Number daalo!"
      return
    try:
      amount = float(amt_str)
      if amount <= 0:
        raise ValueError()
    except ValueError:
      status_label.text = "❌ Error: Sahi Amount dalo!"
      return

    data = load_data()
    if veh not in data["vehicles"]:
      data["vehicles"][veh] = {"total_spent": 0, "transactions": []}

    data["vehicles"][veh]["total_spent"] += amount
    data["vehicles"][veh]["transactions"].append({
        "date": str(date.today()),
        "amount": amount,
        "note": note,
    })
    save_data(data)

    status_label.text = f"✅ Success! ₹{amount} saved for {veh}."
    veh_input.text = ""
    amt_input.text = ""
    note_input.text = ""


class DriverExpenseScreen(Screen):

  def save_drv_expense(self, drv_input, amt_input, note_input, status_label):
    drv = drv_input.text.upper().strip()
    amt_str = amt_input.text.strip()
    note = note_input.text.strip()

    if not drv:
      status_label.text = "❌ Error: Driver Name daalo!"
      return
    try:
      amount = float(amt_str)
      if amount <= 0:
        raise ValueError()
    except ValueError:
      status_label.text = "❌ Error: Sahi Amount dalo!"
      return

    data = load_data()
    if "drivers" not in data:
      data["drivers"] = {}
    if drv not in data["drivers"]:
      data["drivers"][drv] = {"total_spent": 0, "transactions": []}

    data["drivers"][drv]["total_spent"] += amount
    data["drivers"][drv]["transactions"].append({
        "date": str(date.today()),
        "amount": amount,
        "note": note,
    })
    save_data(data)

    status_label.text = f"✅ Success! ₹{amount} saved for {drv}."
    drv_input.text = ""
    amt_input.text = ""
    note_input.text = ""


class DashboardScreen(Screen):

  def on_enter(self):
    data = load_data()
    vehicles = data.get("vehicles", {})
    drivers = data.get("drivers", {})

    report = ""
    if not vehicles and not drivers:
      report = "📂 No Saved Data Yet."
    else:
      if vehicles:
        report += "🚗 VEHICLE EXPENSES:\n"
        for veh, details in vehicles.items():
          report += f" • {veh} | Total: ₹{details['total_spent']}\n"
          for tx in details["transactions"]:
            note_text = f" ({tx['note']})" if tx["note"] else ""
            report += f"   - [{tx['date']}] ₹{tx['amount']}{note_text}\n"
        report += "\n" + "-" * 25 + "\n\n"

      if drivers:
        report += "👨‍✈️ DRIVER EXPENSES:\n"
        for drv, details in drivers.items():
          report += f" • {drv} | Total: ₹{details['total_spent']}\n"
          for tx in details["transactions"]:
            note_text = f" ({tx['note']})" if tx["note"] else ""
            report += f"   - [{tx['date']}] ₹{tx['amount']}{note_text}\n"

    self.ids.report_label.text = report


# --- App UI Design (KV Language) ---
KV = """
ScreenManager:
    MenuScreen:
    VehicleExpenseScreen:
    DriverExpenseScreen:
    DashboardScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20
        Label:
            text: '🚚 FLEET & DRIVER MANAGER'
            font_size: 20
            bold: True
            size_hint_y: None
            height: 50
        Button:
            text: '1. ➕ Enter Vehicle Expense'
            font_size: 16
            on_press: root.manager.current = 'veh_screen'
        Button:
            text: '2. 👨‍✈️ Enter Driver Expense'
            font_size: 16
            on_press: root.manager.current = 'drv_screen'
        Button:
            text: '3. 📊 Check Dashboard'
            font_size: 16
            on_press: root.manager.current = 'dash_screen'

<VehicleExpenseScreen>:
    name: 'veh_screen'
    BoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 10
        Label:
            text: 'Vehicle Expense Entry'
            font_size: 18
            bold: True
            size_hint_y: None
            height: 40
        Label:
            text: 'Vehicle Number:'
            size_hint_y: None
            height: 20
        TextInput:
            id: veh_in
            multiline: False
            size_hint_y: None
            height: 45
        Label:
            text: 'Amount (₹):'
            size_hint_y: None
            height: 20
        TextInput:
            id: amt_in
            multiline: False
            input_filter: 'float'
            size_hint_y: None
            height: 45
        Label:
            text: 'Note / Description:'
            size_hint_y: None
            height: 20
        TextInput:
            id: note_in
            multiline: False
            size_hint_y: None
            height: 45
        Label:
            id: status_lbl
            text: ''
            color: 0, 1, 0, 1
            size_hint_y: None
            height: 30
        Button:
            text: 'Save Entry'
            size_hint_y: None
            height: 45
            on_press: root.save_veh_expense(veh_in, amt_in, note_in, status_lbl)
        Button:
            text: '⬅ Back to Menu'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'menu'

<DriverExpenseScreen>:
    name: 'drv_screen'
    BoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 10
        Label:
            text: 'Driver Expense Entry'
            font_size: 18
            bold: True
            size_hint_y: None
            height: 40
        Label:
            text: 'Driver Name:'
            size_hint_y: None
            height: 20
        TextInput:
            id: drv_in
            multiline: False
            size_hint_y: None
            height: 45
        Label:
            text: 'Amount (₹):'
            size_hint_y: None
            height: 20
        TextInput:
            id: amt_in
            multiline: False
            input_filter: 'float'
            size_hint_y: None
            height: 45
        Label:
            text: 'Note / Description:'
            size_hint_y: None
            height: 20
        TextInput:
            id: note_in
            multiline: False
            size_hint_y: None
            height: 45
        Label:
            id: status_lbl
            text: ''
            color: 0, 1, 0, 1
            size_hint_y: None
            height: 30
        Button:
            text: 'Save Entry'
            size_hint_y: None
            height: 45
            on_press: root.save_drv_expense(drv_in, amt_in, note_in, status_lbl)
        Button:
            text: '⬅ Back to Menu'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'menu'

<DashboardScreen>:
    name: 'dash_screen'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: '📊 Expense Dashboard'
            font_size: 18
            bold: True
            size_hint_y: None
            height: 40
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                Label:
                    id: report_label
                    text: ''
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] if hasattr(self, 'texture_size') else 400
        Button:
            text: '⬅ Back to Menu'
            size_hint_y: None
            height: 45
            on_press: root.manager.current = 'menu'
"""


class FleetManagerApp(App):

  def build(self):
    return Builder.load_string(KV)


if __name__ == "__main__":
  FleetManagerApp().run()