# BioNLP-Toolkit
Commonly used BioNLP toolkit for myself.  

## Split_PubTator_File.py
  **description:** PubTator file split.  
  **option:** PubTator_file, PubTator_num_per_file, Save_path.  

## PubTator_File_Merge.py
  **description:** Integrate two PubTator files and ensure that the PMID is unique.  
  **option:** PubTator_file_a, PubTator_file_b, Merge_file.  

## Multithreaded_call.py  
  **description:** Multi-process calling target function.  
  **option:** Iteration_path, save_path, target_function.  



## Get_ID_from_PMC_PubMed.py
 **get_id(id_file, pmid_save_path)**
  **description:** Use e-utils to automatically obtain the PMCID and PMID of keywords or MeSH entries.
 **extract_pmc_pmid(pmid_save_path, total_id_save_file)**
  **description:** Integrate all the IDs obtained in the previous step into a single file.
```
Input: A folder containing files in the following format, each line (an term) of each file can have one or more keywords.
       e.g.    
       Cancer Type Studied	MESH
       Acute Myeloid Leukemia	D015470
       Adrenocortical Carcinoma	D018268
       Breast Ductal Carcinoma	D018270
Output: Each line generates a file with a corresponding name, and each file contains three columns, namely Term, PMC/PMID and ID Source.
       e.g. 
       Term	PMC/PMID	Source
       Breast Ductal Carcinoma	5259919	PMC
       Breast Ductal Carcinoma	4005628	PMC
```

## PMC_PMID_to_PubTator.py
 **get_annotation(pmid_info_path, pubtator_save_path, id_batch_size)**
  **description:** According to the input ID file, the PubTator annotation files corresponding to PMID and PMC are obtained respectively.
```
Input: The input is a folder containing files in the following format, each file contains three columns, namely Term, PMC/PMID and ID Source, where ID Source is "PMID" or "PMC".
       e.g.
       Term	PMC/PMID	Source
       Bladder Urothelial Carcinoma	32292705	PMID
       Bladder Urothelial Carcinoma	4603215	PMC

OutPut: The output file is PubTator annotation in BioCJson format, you can refer to the following webpage or annotation examples for more details.
        e.g.
        PubTator: https://www.ncbi.nlm.nih.gov/research/pubtator/
        Some examples
        https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=28483577&concepts=gene
        https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735
        https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579
```



