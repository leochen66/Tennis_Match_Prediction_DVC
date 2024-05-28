# Tennis_Match_Prediction_DVC
### Create DVC pipline
```
dvc stage add --force -n data_pull \
                -d workflows/data_pull.py \
		-o data/atp_tennis.csv \
                python workflows/data_pull.py

dvc stage add --force  -n preprocess \
                -d workflow/data_preprocess.py -d data/atp_tennis.csv \
		-o data/train.csv -o data/test.csv \
                python workflows/data_preprocess.py

dvc stage add --force  -n train \
                -d workflow/model_train.py -d data/train.csv -d data/test.csv \
                -o artifacts \
                python workflows/model_train.py

```
### Pipeline
```
>> dvc dag
+-----------+  
| data_pull |  
+-----------+  
       *       
       *       
       *       
+------------+ 
| preprocess | 
+------------+ 
       *       
       *       
       *       
  +-------+    
  | train |    
  +-------+ 

```
run pipline 
```
dvc repro
```

### Data Track
Ask DVC to track data
```
dvc add data/

git add data.dvc .gitignore
git commit -m 
```
Connect local data to remote
```
dvc remote add -d myremote s3://tennis-dataset

dvc push
```