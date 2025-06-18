# 🚀 Intrusion Detection System (IDS) Using Machine Learning

Welcome to my **Intrusion Detection System (IDS)** project! This system leverages **machine learning techniques** to detect and classify network intrusions and cyber-attacks in real time. It is designed to enhance network security by identifying malicious activities such as DoS, DDoS, probe, and ransomware attacks.

---

## 📌 Features

✅ Real-time monitoring of log files (e.g., `access.log`)
✅ Feature extraction: protocol type, service, flag, src\_bytes, dst\_bytes, bytes\_ratio, packet\_size\_diff, etc.
✅ Trained on **KDD 99 dataset** (or NSL-KDD, if applied)
✅ Machine learning model: **Random Forest Classifier** (with high accuracy \~99%)
✅ Modular design with clear separation of log parsing, feature engineering, and prediction
✅ Simulated attack tools (DoS, DDoS, ransomware) for testing
✅ GUI to control and visualize IDS engine (optional if implemented)

---

## 🏗 Project Structure

```
IDS-Project/
│
├── data/                # Dataset files (KDD 99, processed features)
├── models/              # Trained ML models (e.g., RandomForest.pkl)
├── attack_tools/        # Scripts to simulate attacks
├── gui/                 # GUI scripts (if applicable)
├── logs/                # Log files (e.g., access.log)
├── src/                 # Core IDS engine code
│   ├── parser.py        # Log parser
│   ├── feature_engineer.py  # Feature engineering logic
│   ├── model_infer.py   # Model loading and prediction
│   └── ...
├── README.md            # Project documentation (this file)
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Technologies Used

* **Python 3.x**
* **scikit-learn**
* **pandas, numpy**
* **matplotlib / seaborn (for analysis and visualization)**
* **tkinter / PyQt (for GUI, if implemented)**

---

## 📊 Dataset

* **KDD Cup 99 dataset**
* Custom features: `bytes_ratio`, `packet_size_diff`, etc.
* \[Optional] Support for **NSL-KDD** or other real-world datasets

---

## 💻 How to Run

1️⃣ **Clone the repository**

```bash
git clone https://github.com/yourusername/IDS-Project.git
cd IDS-Project
```

2️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

3️⃣ **Run the IDS engine**

```bash
python src/main.py
```

4️⃣ **(Optional) Launch the GUI**

```bash
python gui/app.py
```

---

## 🚨 Attack Simulation

Test your IDS using provided attack tools:

```bash
python attack_tools/dos_simulator.py
python attack_tools/ddos_simulator.py
python attack_tools/ransomware_simulator.py
```

---

## 📝 Future Improvements

* Integration with live network packet captures (e.g., using **Scapy**, **PyShark**)
* Deep learning model integration (e.g., LSTM, CNN)
* Support for additional datasets (NSL-KDD, UNSW-NB15)
* Enhanced GUI with analytics dashboard

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---

## 🙌 Acknowledgements

* [KDD Cup 99 Dataset](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
* Scikit-learn, Pandas, NumPy communities
