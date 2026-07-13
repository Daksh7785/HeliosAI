# Downloading ISSDC PRADAN Data

To use the HeliosAI application with actual Aditya-L1 data, you will need to download the Level-1 FITS files from the ISRO ISSDC PRADAN portal. Follow these steps:

## Prerequisites
1. You must be registered on the [ISSDC PRADAN portal](https://pradan.issdc.gov.in/).
2. You need to log in to access the Aditya-L1 scientific payloads data.

## Step-by-Step Guide

### 1. Navigating to the Payload Data
- After logging in, go to the **Data Search** or **Aditya-L1 Data** section.
- Select the payloads you want to download data for:
  - **SoLEXS** (Solar Low Energy X-ray Spectrometer)
  - **HEL1OS** (High Energy L1 Orbiting X-ray Spectrometer)
- Select the **Processing Level** as `Level-1` (L1).
- Choose a time window (e.g., specific days or months) using the provided calendar widgets.

### 2. Requesting the Data
- Add the desired data granules to your cart.
- Proceed to checkout and submit your data request.
- You will receive a notification (or email) once the data processing is complete and the download links are generated.

### 3. Downloading and Placing the Files
- Download the generated `.fits` files or `.zip` archives.
- If you downloaded `.zip` files, extract them to get the underlying `.fits` files.
- Locate the root directory of the HeliosAI project.
- Move or copy the extracted `.fits` files into the `data/raw/` directory. For example:
  ```
  HeliosAI/
  ├── data/
  │   ├── raw/
  │   │   ├── aditya_l1_solexs_l1_..._v01.fits
  │   │   ├── aditya_l1_helios_l1_..._v01.fits
  ```

### 4. Running the Dashboard
- Once the files are in `data/raw/`, start the application using `streamlit run app.py`.
- On the left sidebar, switch the **Data Source** from `Simulated Data` to `Real ISSDC Data`.
- The application will automatically parse the FITS files, merge the timestamps, and display the live soft and hard X-ray fluxes.

> [!NOTE]
> Ensure you have installed the required dependencies, including `astropy`, which is necessary for parsing the binary table extensions inside the FITS files. You can do this by running `pip install -r requirements.txt`.
