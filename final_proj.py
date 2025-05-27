import pandas as pd
import numpy as np
import scprep, umap, graphtools as gt, phenograph, tasklogger
import matplotlib.pyplot as plt
from sklearn import cluster
%matplotlib inline
%%bash

## Read in the MYELOID counts 
## Explore the data in /home/jovyan/shared/course/bioe-c149-readwrite/hw3
## You should see a file 'Brain_Myeloid-counts.csv'
## Add the path to this file in the function below

# myeloid_data = scprep.io.load_csv("/home/jovyan/shared/course/bioe-c149-readwrite/hw3/Brain_Myeloid-counts.csv",
                          # cell_axis='row', sparse=True).transpose()

# Load Tabula Muris dataset for two tissue types
lung_data = scprep.io.load_csv('Lung-counts.csv', cell_axis='row', sparse=True).transpose()





## NOTE: For future steps, we need the transposed version of the original Myeloid dataset
## which is why you see the call .transpose()

lung_data.head()

## Read in the NON-MYELOID counts 
## Explore the data in /home/jovyan/shared/course/bioe-c149-readwrite/hw3
## You should see a file 'Brain_Non-Myeloid-counts.csv'
## Add the path to this file in the function below


trachea_data = scprep.io.load_csv('Trachea-counts.csv', cell_axis='row', sparse=True).transpose()

display(trachea_data.head())
print(trachea_data.shape)

## Fill the labels appropriately

data = [lung_data, trachea_data]
batch_labels = ['lung', 'trachea']

# Combine datasets
# data, sample_labels = scprep.utils.combine_batches([tissue1_data, tissue2_data], ['tissue1', 'tissue2'])
## This combines batches together into a single DataFrame
data, sample_labels = scprep.utils.combine_batches(data, batch_labels)

lookup = pd.Series(data.index).apply(lambda x: x.split('.')[1])

# print(lookup.values)
## TO DO
## fill in the path to metadata_FACS.csv below
## This file should be in /home/jovyan/shared/course/bioe-c149-readwrite/hw3
metadata = pd.read_csv('metadata_FACS.csv', index_col=0).loc[lookup.values].reset_index()
metadata.index = data.index
print(metadata.index)




# Read annotations file
annotations = pd.read_csv('annotations_facs.csv', dtype=object)

# Clean cell names in annotations to match data index format
annotations['cleaned_cell'] = annotations['cell'].apply(lambda x: x.split('.')[1])

# Filter annotations to only include cells in our data
annotations = annotations[annotations['cleaned_cell'].isin(lookup.values)]

# Remove any duplicates based on cleaned cell names
annotations = annotations.drop_duplicates(subset=['cleaned_cell'])

# Set index to match data index
annotations = annotations.set_index('cleaned_cell')
annotations = annotations.reindex(lookup.values)
annotations.index = data.index

# print(f"Annotations shape: {annotations.shape}")
# print(f"Data shape: {data.shape}")













# ####
# lookup = pd.Series(data.index).apply(lambda x: x.rsplit('_', 1)[0])
# # lookup = pd.Series(data.index).apply(lambda x: x.split('.')[1])
# print(lookup.values)

# # annotations = pd.read_csv('annotations_facs.csv', dtype=object)
# # annotations['cleaned_cell'] = annotations['cell'].rsplit('_', 1)[0]
# # result = data.rsplit('_', 1)[0]
# # annotations['cleaned_cell'] = annotations['cell']
# ## annotations['cleaned_cell'] = annotations['cell']
# annotations = pd.read_csv('annotations_facs.csv', index_col=2, dtype=object).loc[lookup.values].reset_index()

# # annotations_subset = annotations[annotations['cleaned_cell'].isin(lookup.values)]
# # # annotations_subset = annotations[annotations['cell'].isin(lookup.values)]
# # annotations_subset = annotations_subset.drop_duplicates(subset=['cleaned_cell'])
# # # annotations_subset = annotations_subset.drop_duplicates(subset=['cell'])

# # # annotations_subset = annotations_subset.set_index('cleaned_cell').reindex(lookup.values)
# # # annotations_subset.index = data.index

# # # Step 4: Align annotations with data
# # annotations_subset = annotations_subset.set_index('cleaned_cell')
# # # annotations_subset = annotations_subset.set_index('cell')
# annotations_subset = annotations_subset.reindex(data.index)  ####causes NaNs in fields
# # # annotations_subset = annotations_subset.loc[data.index.intersection(annotations_subset.index)]
# # # annotations_subset = annotations_subset.loc[annotations_subset.index.intersection(data.index)]

# # annotations.index = lookup.values
# print(annotations.index)
# # annotations.index = data.index
# # annotations_subset = annotations_subset.loc[annotations_subset.index.intersection(data.index)]

# # annotations = pd.read_csv('annotations_facs.csv', index_col="cell", dtype=object).loc[list(lookup.values)[0]].reset_index()
# # annotations.index = data.index
# # annotations.index = data.index
# ########
# # #####################################
# # # metadata = pd.read_csv('/path/to/metadata_FACS.csv', index_col=0)  # Update with the correct path
# # annotations = pd.read_csv('annotations_facs.csv', index_col=2, dtype=object)  # Update with the correct path

# # # Extract the second portion of the annotations index after the first period
# # annotations_lookup = pd.Series(annotations.index).apply(lambda x: x.split('.')[1])

# # # Create a mapping from the original annotation index to the extracted lookup value
# # annotations_index_map = pd.DataFrame({'original_index': annotations.index, 'lookup': annotations_lookup})

# # # Filter annotations where the lookup value is present in the metadata index
# # matching_annotations = annotations_index_map[annotations_index_map['lookup'].isin(metadata.index)]

# # # Reindex annotations based on the matching lookup values
# # aligned_annotations = annotations.loc[matching_annotations['original_index']]

# # # Reset the index to match the metadata index
# # aligned_annotations.reset_index(drop=True, inplace=True)

# # # Display the aligned annotations
# # print(aligned_annotations.head())

# # #############################################################
# # print("SUBSET: ", annotations_subset.head())

# print(f"Data rows: {data.shape[0]}, Metadata rows: {metadata.shape[0]}, Annotations rows: {aligned_annotations.shape[0]}")

# # print(annotations.head())
# # annotations['cell'] = annotations['cell'].str.strip() 
# # metadata.index = metadata.index.astype(str).str.strip()  # Make sure metadata index is a clean string

# # Step 3: Merge metadata with annotations using 'plate.barcode' or 'cell'
# # combined = metadata.merge(annotations, left_index=True, right_on='plate.barcode', how='left')

# # Step 4: View combined data to check alignment
# # print("Combined DataFrame preview:")
# # print(combined.head())

# #check out what your metadata looks like using head():
# # The data for this homework is from Tabula Muris
# # Learn more about the data here - https://tabula-muris.sf.czbiohub.org ! 
# # Not for submission: What is FACS selection?

# # print(metadata.head())

# annotations.head()

