# 📍 Training Data Setup Guide

## Complete Step-by-Step Instructions for Saving & Loading Training Points

This guide shows you how to export your training points from GEE Code Editor as assets, then load them into your Streamlit app.

---

## 🎯 Overview

Instead of manually copying training points, we'll:
1. ✅ Export training geometries as GEE assets (ONE TIME)
2. ✅ Load them automatically in the Streamlit app
3. ✅ Never have to copy/paste coordinates again

**Time required:** 15 minutes (one-time setup)

---

## Step 1: Export Training Points from GEE Code Editor

### A. Add Export Code to Your JavaScript Tool

Open your original GEE Code Editor script and **add this code at the very end**:

```javascript
// ═══════════════════════════════════════════════════════════════════
// EXPORT TRAINING POINTS AS ASSETS (RUN ONCE)
// ═══════════════════════════════════════════════════════════════════

// Helper function to export training points
function exportTrainingPoints(geometry, year, className) {
  var fc = ee.FeatureCollection(
    geometry.geometries().map(function(geom) {
      return ee.Feature(ee.Geometry(geom), {
        'class': className,
        'year': year
      });
    })
  );
  
  Export.table.toAsset({
    collection: fc,
    description: 'export_' + className + '_' + year,
    assetId: 'users/YOUR_USERNAME/kericho_training/' + className + '_' + year
  });
}

// ═══════════════════════════════════════════════════════════════════
// 1995 TRAINING POINTS
// ═══════════════════════════════════════════════════════════════════
exportTrainingPoints(forest1995, 1995, 'forest');
exportTrainingPoints(tea1995, 1995, 'tea');
exportTrainingPoints(otherveg1995, 1995, 'otherveg');
exportTrainingPoints(bare1995, 1995, 'bare');
exportTrainingPoints(builtup1995, 1995, 'builtup');

// ═══════════════════════════════════════════════════════════════════
// 2005 TRAINING POINTS
// ═══════════════════════════════════════════════════════════════════
exportTrainingPoints(forest2005, 2005, 'forest');
exportTrainingPoints(tea2005, 2005, 'tea');
exportTrainingPoints(otherveg2005, 2005, 'otherveg');
exportTrainingPoints(bare2005, 2005, 'bare');
exportTrainingPoints(builtup2005, 2005, 'builtup');

// ═══════════════════════════════════════════════════════════════════
// 2015 TRAINING POINTS
// ═══════════════════════════════════════════════════════════════════
exportTrainingPoints(forest2015, 2015, 'forest');
exportTrainingPoints(tea2015, 2015, 'tea');
exportTrainingPoints(otherveg2015, 2015, 'otherveg');
exportTrainingPoints(bare2015, 2015, 'bare');
exportTrainingPoints(builtup2015, 2015, 'builtup');

// ═══════════════════════════════════════════════════════════════════
// 2024 TRAINING POINTS
// ═══════════════════════════════════════════════════════════════════
exportTrainingPoints(forest2024, 2024, 'forest');
exportTrainingPoints(tea2024, 2024, 'tea');
exportTrainingPoints(otherveg2024, 2024, 'otherveg');
exportTrainingPoints(bare2024, 2024, 'bare');
exportTrainingPoints(builtup2024, 2024, 'builtup');

// ═══════════════════════════════════════════════════════════════════
print('═══════════════════════════════════════════════════════════════');
print('✅ EXPORT CODE READY!');
print('═══════════════════════════════════════════════════════════════');
print('NEXT STEPS:');
print('1. Look at the Tasks tab (right side) →');
print('2. You should see 20 export tasks');
print('3. Click RUN on each task (or click RUN ALL)');
print('4. Wait 5-10 minutes for all to complete');
print('5. Your training data will be saved as GEE assets');
print('═══════════════════════════════════════════════════════════════');
```

**⚠️ IMPORTANT:** Replace `YOUR_USERNAME` with your actual GEE username!

To find your username:
- Look at the Assets tab (left side of Code Editor)
- It shows: `users/YOUR_USERNAME/`
- Copy that username

### B. Run the Script

1. **Click "Run"** button at top of Code Editor
2. Wait a few seconds for the script to execute
3. Check the Console (right side) - you should see the instructions printed

### C. Execute Export Tasks

1. **Click the "Tasks" tab** (right side, orange icon)
2. You should see **20 tasks** waiting:
   - `export_forest_1995`
   - `export_tea_1995`
   - `export_otherveg_1995`
   - `export_bare_1995`
   - `export_builtup_1995`
   - ... and 15 more for years 2005, 2015, 2024

3. **Click "RUN"** on each task
   - Or hover and click "RUN ALL" if available

4. **Wait for completion** (~5-10 minutes total)
   - Tasks will turn blue (running) then green (completed)
   - You can close the browser - tasks run server-side

### D. Verify Assets Were Created

1. **Go to Assets tab** (left side of Code Editor)
2. **Refresh** if needed (click refresh icon)
3. **Look for folder:** `kericho_training`
4. **Expand the folder** - you should see 20 assets:
   ```
   kericho_training/
   ├── forest_1995
   ├── tea_1995
   ├── otherveg_1995
   ├── bare_1995
   ├── builtup_1995
   ├── forest_2005
   ├── tea_2005
   ├── ... (and 13 more)
   ```

**✅ If you see all 20 assets, you're done with Step 1!**

---

## Step 2: Update Your Streamlit App

### A. Edit `gee_analysis.py`

The file has already been updated! But you need to change **ONE LINE**.

Open `gee_analysis.py` and find line 49 (around the top of `_load_training_data` method):

```python
GEE_USERNAME = 'celestakim019'  # ← CHANGE THIS TO YOUR USERNAME
```

**Replace** `'celestakim019'` with **your actual GEE username**.

Example:
```python
GEE_USERNAME = 'johndoe123'  # If your username is johndoe123
```

**Save the file.**

### B. That's It!

Your app will now automatically load training data from GEE assets.

---

## Step 3: Test the Setup

### Run Your Streamlit App

```bash
streamlit run app.py
```

### Initialize Analysis

1. Click **"🚀 Initialize Analysis"** in sidebar
2. Watch the progress indicators
3. If everything works, you'll see: **"✅ Analysis ready!"**

### Verify Training Data Loaded

Check the terminal/console where Streamlit is running. You should **NOT** see warnings like:
```
Warning: Could not load forest_1995 from users/...
```

If you see warnings, it means:
- ❌ Assets weren't created properly
- ❌ Wrong username in `gee_analysis.py`
- ❌ Assets are in a different location

---

## 🐛 Troubleshooting

### Issue: "Could not load [class]_[year]"

**Cause:** Assets not found

**Solutions:**
1. Check your username is correct in `gee_analysis.py`
2. Verify assets exist in GEE Code Editor Assets tab
3. Check asset path: `users/YOUR_USERNAME/kericho_training/forest_1995`

### Issue: Export tasks failed in GEE

**Cause:** Various GEE errors

**Solutions:**
1. Check if your geometries actually have points (not empty)
2. Try exporting one task manually first to test
3. Check GEE quota hasn't been exceeded

### Issue: "Training data is None"

**Cause:** Assets exist but couldn't be loaded

**Solutions:**
1. Check GEE authentication: `earthengine authenticate`
2. Verify asset permissions (should be accessible to you)
3. Try loading one asset manually in GEE Code Editor to test

### Issue: Some classes work, others don't

**Cause:** Incomplete export

**Solutions:**
1. Check Tasks tab in GEE - did all 20 tasks complete?
2. Re-run failed tasks
3. Check Console for specific error messages

---

## 📁 Asset Structure Reference

Your GEE assets should look like this:

```
users/YOUR_USERNAME/
└── kericho_training/
    ├── forest_1995       (FeatureCollection)
    ├── tea_1995          (FeatureCollection)
    ├── otherveg_1995     (FeatureCollection)
    ├── bare_1995         (FeatureCollection)
    ├── builtup_1995      (FeatureCollection)
    ├── forest_2005       (FeatureCollection)
    ├── tea_2005          (FeatureCollection)
    ├── otherveg_2005     (FeatureCollection)
    ├── bare_2005         (FeatureCollection)
    ├── builtup_2005      (FeatureCollection)
    ├── forest_2015       (FeatureCollection)
    ├── tea_2015          (FeatureCollection)
    ├── otherveg_2015     (FeatureCollection)
    ├── bare_2015         (FeatureCollection)
    ├── builtup_2015      (FeatureCollection)
    ├── forest_2024       (FeatureCollection)
    ├── tea_2024          (FeatureCollection)
    ├── otherveg_2024     (FeatureCollection)
    ├── bare_2024         (FeatureCollection)
    └── builtup_2024      (FeatureCollection)
```

Each FeatureCollection contains:
- Multiple point geometries
- Properties: `class` (string), `year` (number)

---

## ✨ Benefits of This Approach

✅ **No manual copying** - Assets load automatically
✅ **Reusable** - Can use same training data in multiple projects
✅ **Shareable** - Can share assets with collaborators
✅ **Organized** - All training data in one place
✅ **Version control** - Can update/improve training points over time
✅ **Fast** - Assets load much faster than inline geometries

---

## 🔄 Updating Training Data (Future)

If you collect new training points or want to improve existing ones:

1. **Update geometries** in GEE Code Editor
2. **Re-run the export tasks** for changed classes/years
3. **Overwrite existing assets** (same assetId)
4. **Restart Streamlit app** - will automatically use new data

No code changes needed!

---

## 📝 Quick Reference

### Export Script Location
Add to end of your GEE Code Editor JavaScript tool

### Asset Path Format
```
users/YOUR_USERNAME/kericho_training/[classname]_[year]
```

### Classnames
- `forest`
- `tea`
- `otherveg`
- `bare`
- `builtup`

### Years
- `1995`
- `2005`
- `2015`
- `2024`

### Python Configuration
File: `gee_analysis.py`
Line: 49
Change: `GEE_USERNAME = 'your_username_here'`

---

## ✅ Checklist

Before running your app, verify:

- [ ] All 20 export tasks completed successfully in GEE
- [ ] Assets visible in GEE Assets tab under `kericho_training/`
- [ ] Username updated in `gee_analysis.py` (line 49)
- [ ] GEE authenticated: `earthengine authenticate`
- [ ] Dependencies installed: `pip install -r requirements.txt`

**If all checked, you're ready to run!** 🚀

```bash
streamlit run app.py
```

---

**Questions?** Check the troubleshooting section or examine the console output for specific error messages.