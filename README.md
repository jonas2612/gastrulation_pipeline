# Structure
**data**: scripts for creating the atlas and query datasets used in the thesis.

**subsampling**: subsampling the atlas into training and validation datasets.

**scvi**: scripts for training a SCVI model on the atlas. Furthermore scripts for analysing the quality of the integration (scIB).

**scarches**: scripts for integrating query datasets into the altas data through scArches.

**otfm**: script for different OT Flow Matching models based on different embeddings.

**cellrank**: Analysis of trajectory inference on query datasets.



# Links between folders

**data** &rarr; **subsampling** &rarr; **scvi** &rarr; **oftm**

**data** &rarr; **scarches** &rarr; **cellrank**
