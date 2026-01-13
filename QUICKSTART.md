# 🚀 Quick Start Guide

Get the Kericho Forest Analysis Tool running in 5 minutes!

## ⚡ Fast Setup

### 1. Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### 2. Authenticate GEE (2 minutes)

```bash
earthengine authenticate
```

Follow the browser prompts to authorize.

### 3. Add Your Training Data (2 minutes)

**CRITICAL:** You must export your training geometries as GEE assets!

**Full detailed instructions:** See `TRAINING_DATA_SETUP.md`

**Quick version:**

1. **In GEE Code Editor**, add export code (see TRAINING_DATA_SETUP.md)
2. **Run exports** - 20 tasks, takes 5-10 mins
3. **In `gee_analysis.py`**, line 49, change:
   ```python
   GEE_USERNAME = 'YOUR_USERNAME_HERE'  # ← Change this!
   ```

**That's it!** Your training data will load automatically from GEE assets.

**Why this way?**
- ✅ No manual copying of coordinates
- ✅ Reusable across projects
- ✅ Easy to update
- ✅ Much cleaner code

### 4. Run! (30 seconds)

```bash
streamlit run app.py
```

Browser opens automatically at http://localhost:8501

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] GEE authenticated (`earthengine authenticate`)
- [ ] Training geometries added to `gee_analysis.py`
- [ ] App running (`streamlit run app.py`)

## 🎯 First Use

1. **Click "🚀 Initialize Analysis"** in sidebar
2. Wait 1-2 minutes (processing 30 years of satellite data)
3. Explore the 5 analysis modes:
   - 🏠 Home - Quick overview
   - 📈 Land Cover - Detailed statistics
   - 🔄 Change Detection - Transitions between years
   - 🌿 Vegetation - Health indices
   - 🌤️ Climate - Temperature & precipitation

## ⚠️ Common Issues

**"GEE Authentication failed"**
```bash
earthengine authenticate
```

**"Training data is None"**
→ You forgot to add your geometries in step 3!

**Slow first run**
→ Normal! GEE is processing decades of data. Subsequent runs are fast.

## 💡 Pro Tips

- **Cache is your friend:** After initialization, everything is cached
- **Export early:** Download CSV data for backup
- **Map layers:** Toggle visibility using the layer control
- **Multi-year comparison:** Use the change detection module

## 📚 Need More Help?

See the full **README.md** for:
- Detailed setup instructions
- Troubleshooting guide
- Technical specifications
- Feature documentation

---

**You're ready!** Launch the tool and start analyzing. 🌲