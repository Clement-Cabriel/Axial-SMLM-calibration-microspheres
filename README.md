# Axial-SMLM-calibration-microspheres

This code is provided as supporting material for the related article: Clément Cabriel, Nicolas Bourg, Guillaume Dupuis, and Sandrine Lévêque-Fort, 'Aberration-accounting calibration for 3D single-molecule localization microscopy', Optics Letters Vol. 43, Issue 2, pp. 174-177 (2018). DOI: https://doi.org/10.1364/OL.43.000174

This code should be used to generate the astigmatism calibration curve from an acquisition of microspheres coated with fluorophores. It means to convert the localization output file (i.e. the list of coordinates corresponding to all the molecules localized) into a calibration curve for the astigmatism that may be used in subsequent experiments.

Please use the following contact inforamtion if you would like to comment or contribute to our work, or if you have problems running the codes or questions about the technique or the data and processing steps: Clément Cabriel: clement.cabriel@espci.fr, cabriel.clement@gmail.com.
If you use this software, please cite the original article. All further work and publication based on this software should follow the licence terms mentioned in the Github repository.

How to use the code:
- Set the input parameters (path to the localization file, measured center and radius of the microsphere in the same coordinate system as the localizationn file, display options, smoothing and croppping). Note: a data sample is provided to test the code (corresponding to the acquisition presented in the article, i.e. 15µm diameter microspheres coated with biotin, and further functionalized with Alexa Fluor 647 and imaged in a dSTORM buffer with an astigmatic detecttion system).
- Run the code. An output calibration file will be generated, which can be used in subsequent experiments.
