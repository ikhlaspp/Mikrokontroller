# Proyek Mikrokontroler - Kontrol Motor & AI PID

Proyek pembelajaran mikrokontroler yang mencakup kontrol motor on/off, komunikasi MQTT, dan implementasi kontrol PID berbasis AI menggunakan machine learning.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Struktur Proyek](#struktur-proyek)
- [Persyaratan](#persyaratan)
- [Instalasi](#instalasi)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Modul-Modul](#modul-modul)

## ✨ Fitur Utama

- **Kontrol Motor Dasar**: Kontrol on/off motor menggunakan Arduino dan Python
- **MQTT Integration**: Komunikasi motor melalui protokol MQTT
- **Kontrol PID AI**: Implementasi kontrol PID dengan optimasi berbasis machine learning (XGBoost)
- **Multi-Platform**: Support Arduino (C++) dan Python

## 📁 Struktur Proyek

```
mikrokontroler/
├── EAS/                           # Evaluasi Akhir Semester
├── ETS/                           # Evaluasi Tengah Semester
│   ├── Modul_1/                   # Motor On/Off Dasar
│   │   ├── motor-on-off.ino
│   │   └── motor-on-off.py
│   └── Modul_2/                   # Motor MQTT
│       └── mtqq_motor-on-off.ino
└── Project/                       # Proyek Utama
    ├── motor_on_off_mtqq/         # Motor dengan MQTT
    │   └── mtqq_motor-on-off/
    │       └── mtqq_motor-on-off.ino
    ├── motor_on_off_python/       # Motor Python
    │   ├── motor-on-off.py
    │   └── motor-on-off/
    │       └── motor-on-off.ino
    └── pid_ai/                    # PID dengan AI (XGBoost)
        ├── ai_pid_python.py
        ├── imclab.py
        ├── train_pid_xgboost.ipynb
        └── imclab_arduino_python/
            └── imclab_arduino_python.ino
```

## 🔧 Persyaratan

### Hardware
- Mikrokontroler Arduino (Uno, Mega, atau kompatibel)
- Motor DC dengan driver (L298N atau sejenisnya)
- Module MQTT (opsional untuk fitur MQTT)
- Kabel dan resistor (sesuai kebutuhan)

### Software
- Arduino IDE (untuk upload kode Arduino)
- Python 3.7+
- Library Python: `paho-mqtt`, `xgboost`, `pandas`, `numpy`

## 📦 Instalasi

### Setup Arduino
1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Hubungkan Arduino ke komputer via USB
3. Pilih Board dan Port yang sesuai
4. Upload sketch dari folder `Modul_1/` atau `Project/`

### Setup Python
```bash
# Install dependencies
pip install paho-mqtt xgboost pandas numpy scikit-learn

# Atau menggunakan requirements (jika ada)
pip install -r requirements.txt
```

## 🚀 Panduan Penggunaan

### 1. Motor On/Off Dasar (Modul 1)

**Arduino:**
```cpp
// Upload motor-on-off.ino ke Arduino
// Koneksi:
// - Motor + ke pin 9
// - Motor - ke GND
```

**Python:**
```bash
python Modul_1/motor-on-off.py
```

### 2. Motor dengan MQTT (Modul 2)

```bash
# Pastikan MQTT Broker berjalan
# Upload mtqq_motor-on-off.ino ke Arduino
# Arduino akan terhubung ke MQTT Broker
```

### 3. Kontrol PID dengan AI

```bash
# Training model XGBoost
jupyter notebook Project/pid_ai/train_pid_xgboost.ipynb

# Jalankan PID dengan AI
python Project/pid_ai/ai_pid_python.py
```

## 📚 Modul-Modul

### Modul 1: Motor On/Off Dasar
- File: `ETS/Modul_1/`
- Deskripsi: Kontrol dasar motor DC on/off
- Implementasi: Arduino (C++) & Python

### Modul 2: Motor MQTT
- File: `ETS/Modul_2/`
- Deskripsi: Kontrol motor via protokol MQTT
- Implementasi: Arduino dengan MQTT client

### Project: Motor On/Off Python
- File: `Project/motor_on_off_python/`
- Deskripsi: Implementasi lengkap kontrol motor dengan Python

### Project: Motor MQTT
- File: `Project/motor_on_off_mtqq/`
- Deskripsi: Kontrol motor melalui MQTT Broker

### Project: PID dengan AI (XGBoost)
- File: `Project/pid_ai/`
- Deskripsi: Kontrol PID optimal menggunakan machine learning
- Fitur:
  - Training model XGBoost untuk parameter PID
  - Testing dan validasi sistem
  - Integrasi dengan Arduino

## 📊 Teknologi yang Digunakan

- **Mikrokontroler**: Arduino
- **Bahasa**: C++, Python
- **Protocol**: MQTT, Serial Communication
- **Machine Learning**: XGBoost, Scikit-learn
- **Tools**: Arduino IDE, Jupyter Notebook

## 💡 Tips & Trik

- Gunakan Serial Monitor untuk debugging kode Arduino
- Pastikan MQTT Broker sudah berjalan sebelum menjalankan kode MQTT
- Test kontrol motor dasar sebelum menggunakan MQTT atau AI
- Calibrate PID parameter menggunakan training XGBoost untuk hasil optimal

## 📝 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran semester 5 Mikrokontroler.

## 👤 Kontributor

- Mahasiswa: Semester 5 - Program Mikrokontroler

---

**Last Updated**: Desember 2025

Untuk pertanyaan atau kontribusi, silakan buat issue atau pull request.
