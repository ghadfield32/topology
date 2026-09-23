# Stage 00 — coding practice solutions

Attempt the learner notebook first. The following code and checks are the canonical reference, with limited declared input assumptions.

## 00.C1 — Read the dimensions

Return (number of observations, number of features) for a nonempty rectangular list. Do not count labels as features.

```python
def table_shape(rows):
    return len(rows), len(rows[0])
```

A table has two different dimensions. The 150 rows are samples; the four columns are measurements of each sample. A two-dimensional array can therefore represent points in four-dimensional feature space.

### Visible checks
```python
assert table_shape([[1,2],[3,4],[5,6]]) == (3,2)
X=load_iris_data().iloc[:,1:5].to_numpy()
assert table_shape(X.tolist()) == (150,4)
print("Measured Iris feature table:",table_shape(X.tolist()))
```

## 00.C2 — Calculate a mean without a library

For a nonempty rectangular numeric table, calculate the arithmetic mean of column j using a loop and division.

```python
def column_mean(rows, j):
    total=0.0
    for row in rows:
        total += row[j]
    return total/len(rows)
```

The loop visits observations, not features. The result summarizes this supplied dataset. It does not establish the mean for every flower in the population.

### Visible checks
```python
assert column_mean([[1,9],[3,7]],0)==2
X=load_iris_data().iloc[:,1:5].to_numpy()
assert np.isclose(column_mean(X,0),np.mean(X[:,0]))
print("Mean sepal length in this snapshot (cm):",column_mean(X,0))
```

## 00.C3 — Turn ink into an entrance value

The supplied digits have intensity 0..16. Return f=1-image/16 as a floating-point array so dark ink enters a sublevel filtration first.

```python
def ink_entrance(image):
    return 1.0-np.asarray(image,dtype=float)/16.0
```

This uses the documented physical encoding range, not a mean or maximum fitted using test observations. The word sublevel means that cells with smaller values enter earlier.

### Visible checks
```python
assert np.allclose(ink_entrance([[0,8,16]]),[[1,.5,0]])
image,sample_id=digit_example(0)
f=ink_entrance(image)
assert f.shape==(8,8) and f.min()>=0 and f.max()<=1
print("Training image",sample_id,"entrance range:",float(f.min()),float(f.max()))
```

## 00.C4 — Separate measurements from labels

Return X and y from the bundled Iris DataFrame. X contains exactly the four *_cm measurements; y is the label. Do not include sample_id or species in X.

```python
def iris_xy(frame):
    names=['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm']
    return frame[names].to_numpy(dtype=float),frame['label'].to_numpy()
```

An identifier is useful for provenance, not automatically a coordinate. A label is a prediction target or an annotation. Inserting it into a supposedly unsupervised distance calculation changes the question.

### Visible checks
```python
X,y=iris_xy(load_iris_data())
assert X.shape==(150,4) and y.shape==(150,)
assert np.array_equal(np.unique(y),[0,1,2])
print("X shape",X.shape,"y shape",y.shape)
```

## 00.C5 — Count a recorded category

Count how many entries of a one-dimensional label array equal a requested value. Use the training split only in the real-data check.

```python
def count_label(labels, wanted):
    return sum(int(label==wanted) for label in labels)
```

Class counts help you understand the sample distribution before a model is fitted. The check does not open the held-out images.

### Visible checks
```python
assert count_label([0,1,0,2],0)==2
images,labels,ids=load_digit_data('train')
counts=[count_label(labels,k) for k in range(10)]
assert sum(counts)==1077
print("Training class counts:",counts)
```

