
# **Bioinformatics Assignments** 🧬💻  
*Curated with ❤️ by [Oneza Hassan](https://github.com/oneza-hassan)*  
![GitHub License](https://img.shields.io/github/license/oneza-hassan/Bioinformatics-Assignments?color=blue)  

Welcome to my collection of **Bioinformatics assignments** completed during my final year of **BS Bioinformatics (BS BIF)** at **Quaid-i-Azam University (QAU)**. This repository showcases hands-on projects spanning functional genomics, enzyme kinetics, molecular modeling, pharmacoinformatics, systems biology, data visualization, and R-based analyses.  

---

## **📂 Repository Structure**  
```
Bioinformatics-Assignments/
├── Functional_Genomics/          # CLI-based assignments (eFetch, etc.)
├── Enzyme_Kinetics/              # Learning resources & analyses
├── Modeling_and_Simulation/      # Homology modeling (SWISS-Model, PDB comparisons)
├── Pharmacoinformatics/          # Python project on domain interactions + resources
├── Systems_Biology/              # SMILES, RNA secondary structure (Nussinov algo)
├── Graphics_and_Visualization/   # OpenGL projects (dot plots, 3D modeling)
├── R_Project/                    # RNA-seq analysis with DESeq2, GEOquery
└── LICENSE                       # MIT License
```

---

## **🔍 Key Projects**  

### **1. Functional Genomics**  
- **CLI-based workflows** using `efetch` and other bioinformatics tools.  
- Example: Gene data retrieval and analysis pipelines.  

### **2. Modeling & Simulation**  
- **Homology modeling** of *Human 4-aminobutyrate* using SWISS-Model.  
- **Template comparison** (PDB: `4y0h`) and structure validation.  

### **3. Pharmacoinformatics (Python Project)**  
- **Domain Interaction Analysis**: Filters MD simulation data by domain ranges (e.g., `ZN1-ZN3`).  
- Outputs organized `.xlsx` files with residue validation logic.  

### **4. Systems Biology**  
- **SMILES** for chemical structures.  
- **RNA secondary structure prediction** using the **Nussinov algorithm**.  

### **5. Graphics and Visualization (OpenGL)**  
- **3D Modeling & Algorithms**:  
  - `bigdipper.cpp`: Star constellation visualization.  
  - `dotplots.cpp`: Sequence alignment dot plots.  
  - `house.cpp`, `polylinegraph.cpp`: Computer graphics practices.  

### **6. R Project (RNA-seq Analysis)**  
- **Differential Gene Expression** using `DESeq2` and `GEOquery`:  
  ```r
  # Key steps:
  data <- getGEO(GEO = "GSE152075")  # Fetch GEO dataset
  dds <- DESeqDataSetFromMatrix(countData = raw_counts, colData = clindata, design = ~positivity)
  res <- results(dds)  # DEG analysis
  plotMA(res)          # Volcano plot
  ```
- **Data Wrangling**:  
  - Renaming metadata columns (`batch`, `positivity`).  
  - Matching sample IDs between counts and clinical data.  
- **Visualizations**: PCA, MA plots, and more.  

---

## **🛠️ Tech Stack**  
- **Languages**: Python, R, Bash, C++ (OpenGL)  
- **Tools**: SWISS-Model, Chimera, PyMOL, DESeq2, GEOquery, ggplot2  
- **Data Formats**: PDB, FASTA, SDF, XLSX, CSV  

---

## **🤝 Contributions Welcome!**  
Found an error or have suggestions? **Pull requests are appreciated!**  
1. Fork the repo.  
2. Create a branch (`git checkout -b improve-feature`).  
3. Commit changes (`git commit -m 'Add new analysis'`).  
4. Push (`git push origin improve-feature`).  
5. Open a **Pull Request**.  

---

## **📜 License**  
MIT License — See [LICENSE](LICENSE).  

---

## **🌐 Connect**  
- **Email**: [onezahassan27@gmail.com](mailto:onezahassan27@gmail.com)  
- **LinkedIn**: [Oneza Hassan Alvi](https://www.linkedin.com/in/oneza-hassan-alvi-5984222bb/)  

*Made with late-night caffeine and a love for bioinformatics!* ☕🧬  

--- 

### **🎉 Happy Coding!**  
![Bioinformatics](https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif)  

---
