## FILES AND DIRECTORIES
- level_c.ipynb - `notebook contains text preprocessing, text encoding and models evaluation and model selection for all classifiers (product, sub-product, issue, sub-issue)`

- complaint-classification-app (dir) - `API for complaint prediction`




## DEPLOYMENT
- API deployed in heroku

API FOR COMPLAINT CLASSIFICATION
```bash
curl -X 'POST' 'https://complaint-classifcation.herokuapp.com/predict' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"complaint": "your complaint" }' 
```

RESPONSE FORMAT
```json
{
  "product" : "Credit reporting",
  "sub_product" : "Credit reporting",
  "issue" : "Improper use of your report",
  "sub_issue":"Credit inquiries on your report that you don't recognize"
}

```

